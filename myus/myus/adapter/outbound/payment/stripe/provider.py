import stripe
from datetime import datetime, timezone
from typing import Any, assert_never
from django.conf import settings
from myus.domain.payment.event.data import PaymentEventContent, PaymentFailedContent, ProviderSubscriptionData, RefundContent
from myus.domain.payment.provider.data import CancelFailed, CancelResult, CancelSuccess, CheckoutCreated, CheckoutData, CheckoutFailed, CheckoutResult, CheckoutSessionData, PaymentMethodSessionCreated, PaymentMethodSessionFailed, PaymentMethodSessionResult, PlanChangeFailed, PlanChangeResult, PlanChangeSuccess, RevokeFailed, RevokeResult, RevokeSuccess, WebhookVerified, WebhookVerifyFailed, WebhookVerifyResult
from myus.domain.payment.provider.interface import PaymentInterface
from myus.utils.common.logger import log
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.i18n import Locale
from myus.utils.enum.payment import CancelError, CheckoutError, PaymentMethodSessionError, PaymentProvider, PlanChangeError, RevokeError, WebhookEventType, WebhookVerifyError
from ._convert import convert_stripe_balance, convert_stripe_event, convert_stripe_paid, convert_stripe_params, convert_stripe_payout, convert_stripe_subscription, stripe_id, stripe_locale, stripe_period_end, stripe_price_id
from ._type import stripe_event_type


class StripeProvider(PaymentInterface):
    @Result.shield_exception()
    def create_checkout(self, input: CheckoutData) -> Result[CheckoutResult, FatalError]:
        params = convert_stripe_params(input)
        if isinstance(params, CheckoutFailed):
            return Result.ok(params)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.create(**params)
        except stripe.APIConnectionError as e:
            log.error("Stripe network error", exc=e)
            return Result.ok(CheckoutFailed(error=CheckoutError.NETWORK_ERROR, message=str(e)))
        except stripe.StripeError as e:
            log.error("Stripe checkout error", exc=e)
            return Result.ok(CheckoutFailed(error=CheckoutError.PROVIDER_REJECTED, message=str(e)))

        if session.url is None or session.id is None:
            log.error("Stripe session missing url or id")
            return Result.ok(CheckoutFailed(error=CheckoutError.PROVIDER_REJECTED, message="missing url or id in session"))

        return Result.ok(CheckoutCreated(session=CheckoutSessionData(
            provider=PaymentProvider.STRIPE,
            external_id=session.id,
            redirect_url=session.url,
        )))

    @Result.shield_exception()
    def verify_webhook(self, payload: bytes, signature: str) -> Result[WebhookVerifyResult, FatalError]:
        try:
            event = stripe.Webhook.construct_event(payload, signature, settings.STRIPE_WEBHOOK_SECRET)
        except stripe.SignatureVerificationError as e:
            log.warning("Stripe webhook signature invalid", exc=e)
            return Result.ok(WebhookVerifyFailed(error=WebhookVerifyError.INVALID_SIGNATURE, message=str(e)))
        except ValueError as e:
            log.warning("Stripe webhook payload malformed", exc=e)
            return Result.ok(WebhookVerifyFailed(error=WebhookVerifyError.MALFORMED_PAYLOAD, message=str(e)))

        event_type = stripe_event_type(event.type)
        if event_type is None:
            return Result.ok(WebhookVerifyFailed(error=WebhookVerifyError.UNSUPPORTED_EVENT, message=f"unsupported event_type={event.type}"))

        stripe.api_key = settings.STRIPE_SECRET_KEY
        event_content = stripe_event_content(event_type, event.data.object.to_dict())
        if event_content is None:
            return Result.ok(WebhookVerifyFailed(error=WebhookVerifyError.UNSUPPORTED_EVENT, message=f"no payment event_type={event.type} event_id={event.id}"))

        external_id, content = event_content
        return Result.ok(WebhookVerified(event=convert_stripe_event(event, event_type, payload, external_id, content)))

    @Result.shield_exception()
    def cancel_subscription(self, external_id: str, idempotency_key: str) -> Result[CancelResult, FatalError]:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            subscription = stripe.Subscription.modify(external_id, cancel_at_period_end=True, idempotency_key=idempotency_key)
        except stripe.InvalidRequestError as e:
            log.warning("Stripe subscription not found for cancel", external_id=external_id, exc=e)
            return Result.ok(CancelFailed(error=CancelError.NOT_FOUND, message=str(e)))
        except stripe.APIConnectionError as e:
            log.error("Stripe network error on cancel", exc=e)
            return Result.ok(CancelFailed(error=CancelError.NETWORK_ERROR, message=str(e)))
        except stripe.StripeError as e:
            log.error("Stripe cancel error", exc=e)
            return Result.ok(CancelFailed(error=CancelError.PROVIDER_REJECTED, message=str(e)))

        return Result.ok(CancelSuccess(
            canceled_at=datetime.now(timezone.utc),
            period_end=stripe_period_end(subscription),
        ))

    @Result.shield_exception()
    def revoke_cancellation(self, external_id: str) -> Result[RevokeResult, FatalError]:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            subscription = stripe.Subscription.modify(external_id, cancel_at_period_end=False)
        except stripe.InvalidRequestError as e:
            log.warning("Stripe subscription not found for revoke", external_id=external_id, exc=e)
            return Result.ok(RevokeFailed(error=RevokeError.NOT_FOUND, message=str(e)))
        except stripe.APIConnectionError as e:
            log.error("Stripe network error on revoke", exc=e)
            return Result.ok(RevokeFailed(error=RevokeError.NETWORK_ERROR, message=str(e)))
        except stripe.StripeError as e:
            log.error("Stripe revoke error", exc=e)
            return Result.ok(RevokeFailed(error=RevokeError.PROVIDER_REJECTED, message=str(e)))

        return Result.ok(RevokeSuccess(subscription=convert_stripe_subscription(subscription)))

    @Result.shield_exception()
    def change_plan(self, external_id: str, product_code: str) -> Result[PlanChangeResult, FatalError]:
        price_id = stripe_price_id(product_code)
        if len(price_id) == 0:
            return Result.ok(PlanChangeFailed(error=PlanChangeError.UNKNOWN_PRODUCT, message=f"price_id not configured for product_code={product_code}"))

        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            current = stripe.Subscription.retrieve(external_id)
            item_id = current["items"]["data"][0]["id"]
            subscription = stripe.Subscription.modify(
                external_id,
                items=[{"id": item_id, "price": price_id}],
                metadata={"product_code": product_code},
                proration_behavior="create_prorations",
            )
        except stripe.InvalidRequestError as e:
            log.warning("Stripe subscription not found for plan change", external_id=external_id, exc=e)
            return Result.ok(PlanChangeFailed(error=PlanChangeError.NOT_FOUND, message=str(e)))
        except stripe.APIConnectionError as e:
            log.error("Stripe network error on plan change", exc=e)
            return Result.ok(PlanChangeFailed(error=PlanChangeError.NETWORK_ERROR, message=str(e)))
        except stripe.StripeError as e:
            log.error("Stripe plan change error", exc=e)
            return Result.ok(PlanChangeFailed(error=PlanChangeError.PROVIDER_REJECTED, message=str(e)))

        return Result.ok(PlanChangeSuccess(subscription=convert_stripe_subscription(subscription)))

    @Result.shield_exception()
    def get_subscription(self, external_id: str) -> Result[ProviderSubscriptionData, FatalError]:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(external_id)
        return Result.ok(convert_stripe_subscription(subscription))

    @Result.shield_exception()
    def create_payment_method_session(self, customer_id: str, return_url: str, locale: Locale) -> Result[PaymentMethodSessionResult, FatalError]:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
                locale=stripe_locale(locale),
                flow_data={"type": "payment_method_update", "after_completion": {"type": "redirect", "redirect": {"return_url": return_url}}},
            )
        except stripe.InvalidRequestError as e:
            log.warning("Stripe customer not found for payment method", customer_id=customer_id, exc=e)
            return Result.ok(PaymentMethodSessionFailed(error=PaymentMethodSessionError.NOT_FOUND, message=str(e)))
        except stripe.APIConnectionError as e:
            log.error("Stripe network error on payment method", exc=e)
            return Result.ok(PaymentMethodSessionFailed(error=PaymentMethodSessionError.NETWORK_ERROR, message=str(e)))
        except stripe.StripeError as e:
            log.error("Stripe payment method error", exc=e)
            return Result.ok(PaymentMethodSessionFailed(error=PaymentMethodSessionError.PROVIDER_REJECTED, message=str(e)))

        return Result.ok(PaymentMethodSessionCreated(redirect_url=session.url))


def stripe_event_content(event_type: WebhookEventType, obj: dict[str, Any]) -> tuple[str, PaymentEventContent] | None:
    match event_type:
        case WebhookEventType.SUBSCRIPTION_CREATED | WebhookEventType.SUBSCRIPTION_UPDATED | WebhookEventType.SUBSCRIPTION_CANCELED:
            subscription = stripe.Subscription.construct_from(obj, stripe.api_key)
            return subscription.id, convert_stripe_subscription(subscription)
        case WebhookEventType.PAYMENT_SUCCEEDED:
            invoice = stripe.Invoice.construct_from(obj, stripe.api_key)
            if invoice.amount_paid == 0:
                return None

            payment_intent_id = stripe_invoice_payment_intent_id(invoice, "paid")
            if len(payment_intent_id) == 0:
                return None

            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id, expand=["latest_charge.balance_transaction"])
            charge = payment_intent.latest_charge
            if not isinstance(charge, stripe.Charge) or not isinstance(charge.balance_transaction, stripe.BalanceTransaction):
                raise ValueError(f"balance_transaction missing payment_intent={payment_intent.id}")
            return payment_intent.id, convert_stripe_paid(invoice, charge.balance_transaction)
        case WebhookEventType.PAYMENT_FAILED:
            invoice = stripe.Invoice.construct_from(obj, stripe.api_key)
            payment_intent_id = stripe_invoice_payment_intent_id(invoice, "open")
            if len(payment_intent_id) == 0:
                return None

            return payment_intent_id, PaymentFailedContent()
        case WebhookEventType.REFUND_ISSUED:
            charge = stripe.Charge.construct_from(obj, stripe.api_key)
            payment_intent_id = stripe_id(charge.payment_intent)
            if len(payment_intent_id) == 0:
                return None

            refunds = stripe.Refund.list(charge=charge.id, expand=["data.balance_transaction"]).auto_paging_iter()
            balances = [convert_stripe_balance(r.balance_transaction) for r in refunds if isinstance(r.balance_transaction, stripe.BalanceTransaction)]
            return payment_intent_id, RefundContent(balances=balances)
        case WebhookEventType.PAYOUT_PAID:
            payout = stripe.Payout.construct_from(obj, stripe.api_key)
            balance_transactions = stripe.BalanceTransaction.list(payout=payout.id).auto_paging_iter()
            balance_external_ids = [b.id for b in balance_transactions if b.type != "payout"]
            return payout.id, convert_stripe_payout(payout, balance_external_ids)
        case _:
            assert_never(event_type)


def stripe_invoice_payment_intent_id(invoice: stripe.Invoice, status: str) -> str:
    payments = stripe.InvoicePayment.list(invoice=invoice.id, status=status)
    payment_intent_ids = [stripe_id(p.payment.payment_intent) for p in payments.data if p.payment.payment_intent is not None]
    if len(payment_intent_ids) == 0:
        return ""
    return payment_intent_ids[0]
