import stripe
from django.conf import settings
from api.modules.logger import log
from api.src.adapter.external.payment.stripe._convert import convert_stripe_event, convert_stripe_params
from api.src.domain.interface.payment.provider.data import CheckoutCreated, CheckoutData, CheckoutFailed, CheckoutResult, CheckoutSessionData, WebhookVerified, WebhookVerifyFailed, WebhookVerifyResult
from api.src.domain.interface.payment.provider.interface import PaymentInterface
from api.utils.enum.payment import CheckoutError, PaymentProvider, WebhookVerifyError


class StripeProvider(PaymentInterface):
    def create_checkout(self, input: CheckoutData) -> CheckoutResult:
        params = convert_stripe_params(input)
        if isinstance(params, CheckoutFailed):
            return params

        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.create(**params)
        except stripe.APIConnectionError as e:
            log.error("Stripe network error", exc=e)
            return CheckoutFailed(error=CheckoutError.NETWORK_ERROR, message=str(e))
        except stripe.StripeError as e:
            log.error("Stripe checkout error", exc=e)
            return CheckoutFailed(error=CheckoutError.PROVIDER_REJECTED, message=str(e))

        if session.url is None or session.id is None:
            log.error("Stripe session missing url or id")
            return CheckoutFailed(error=CheckoutError.PROVIDER_REJECTED, message="missing url or id in session")

        return CheckoutCreated(session=CheckoutSessionData(
            provider=PaymentProvider.STRIPE,
            external_id=session.id,
            redirect_url=session.url,
        ))

    def verify_webhook(self, payload: bytes, signature: str) -> WebhookVerifyResult:
        try:
            event = stripe.Webhook.construct_event(payload, signature, settings.STRIPE_WEBHOOK_SECRET)  # type: ignore[no-untyped-call]
        except stripe.SignatureVerificationError as e:
            log.warning("Stripe webhook signature invalid", exc=e)
            return WebhookVerifyFailed(error=WebhookVerifyError.INVALID_SIGNATURE, message=str(e))
        except ValueError as e:
            log.warning("Stripe webhook payload malformed", exc=e)
            return WebhookVerifyFailed(error=WebhookVerifyError.MALFORMED_PAYLOAD, message=str(e))

        event_data = convert_stripe_event(event)
        if isinstance(event_data, WebhookVerifyFailed):
            return event_data
        return WebhookVerified(event=event_data)
