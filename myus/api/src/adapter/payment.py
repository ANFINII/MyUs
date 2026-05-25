from dataclasses import replace
from django.conf import settings
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.domain.interface.payment.data import Money
from api.src.domain.interface.payment.provider.data import CancelFailed, CancelSuccess, CheckoutCreated, CheckoutData, CheckoutFailed, CustomerData, MarketplaceData, RedirectUrls, WebhookVerified, WebhookVerifyFailed
from api.src.domain.interface.payment.provider.interface import PaymentInterface
from api.src.domain.interface.payment.subscription.interface import FilterOption as SubscriptionFilterOption, SortOption as SubscriptionSortOption, SubscriptionInterface
from api.src.domain.interface.webhook.inbox.interface import FilterOption, SortOption, WebhookInboxInterface
from api.src.injectors.container import injector
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.payment import PaymentCancelOut, PaymentCheckoutIn, PaymentCheckoutOut, PaymentWebhookOut
from api.src.usecase.auth import auth_check
from api.src.usecase.payment import handle_webhook_event
from api.src.usecase.user import get_user_data
from api.utils.enum.i18n import Currency, Locale
from api.utils.enum.payment import PaymentProvider, PaymentType, SubscriptionStatus, WebhookVerifyError
from api.utils.plan import get_plan


class PaymentAPI:
    """料金プランAPI"""

    router = Router()

    @staticmethod
    @router.post("/checkout", response={200: PaymentCheckoutOut, 401: ErrorOut, 404: ErrorOut, 500: ErrorOut})
    def checkout(request: HttpRequest, input: PaymentCheckoutIn):
        log.info("PaymentAPI checkout", plan=input.plan)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        user_data = get_user_data(user_id=user_id)
        if user_data is None:
            return 404, ErrorOut(message="Not Found")

        plan = get_plan(input.plan)
        if plan is None:
            log.warning("PaymentAPI unknown plan", plan=input.plan)
            return 404, ErrorOut(message="Not Found")

        data = CheckoutData(
            product_code=plan.name,
            description=plan.description,
            price=Money(amount=plan.price, currency=Currency.JPY),
            payment_type=PaymentType.SUBSCRIPTION,
            customer=CustomerData(email=user_data.user.email),
            redirect=RedirectUrls(
                success_url=f"{settings.FRONTEND_URL}/setting/payment/success",
                cancel_url=f"{settings.FRONTEND_URL}/setting/payment",
            ),
            marketplace=MarketplaceData(seller_id="", application_fee=Money(amount=0, currency=Currency.JPY)),
            locale=Locale.JA,
        )

        payment = injector.get(PaymentInterface)
        result = payment.create_checkout(data)
        match result:
            case CheckoutCreated(session=session):
                return 200, PaymentCheckoutOut(url=session.redirect_url)
            case CheckoutFailed(error=error, message=message):
                log.error("Payment checkout failed", error=error.value, message=message)
                return 500, ErrorOut(message="決済セッションの作成に失敗しました!")

    @staticmethod
    @router.post("/webhook", response={200: PaymentWebhookOut, 400: ErrorOut})
    def webhook(request: HttpRequest):
        payload = request.body
        signature = request.META.get("HTTP_STRIPE_SIGNATURE", "")

        payment = injector.get(PaymentInterface)
        verify_result = payment.verify_webhook(payload, signature)

        match verify_result:
            case WebhookVerifyFailed(error=WebhookVerifyError.UNSUPPORTED_EVENT, message=message):
                log.info("PaymentAPI webhook unsupported event", message=message)
                return 200, PaymentWebhookOut(message="Unsupported event type")
            case WebhookVerifyFailed(error=error, message=message):
                log.warning("PaymentAPI webhook verify failed", error=error.value, message=message)
                return 400, ErrorOut(message="Invalid webhook")
            case WebhookVerified(event=event):
                log.info("PaymentAPI webhook verified", event_id=event.event_id, event_type=event.event_type.value)

                webhook_event_repo = injector.get(WebhookInboxInterface)
                existing_ids = webhook_event_repo.get_ids(
                    FilterOption(provider=event.provider.value, event_id=event.event_id),
                    SortOption(),
                    limit=1,
                )
                if len(existing_ids) > 0:
                    log.info("PaymentAPI webhook already processed", event_id=event.event_id)
                    return 200, PaymentWebhookOut(message="Already processed")

                webhook_event_repo.bulk_save([event])
                handle_webhook_event(event)
                return 200, PaymentWebhookOut(message="OK")

    @staticmethod
    @router.post("/cancel", response={200: PaymentCancelOut, 401: ErrorOut, 404: ErrorOut, 500: ErrorOut})
    def cancel(request: HttpRequest):
        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        sub_repo = injector.get(SubscriptionInterface)
        ids = sub_repo.get_ids(
            SubscriptionFilterOption(customer_user_id=user_id, provider=PaymentProvider.STRIPE.value),
            SubscriptionSortOption(is_asc=False),
            limit=1,
        )
        if len(ids) == 0:
            return 404, ErrorOut(message="アクティブなサブスクリプションが見つかりません")

        subs = sub_repo.bulk_get(ids)
        subscription = subs[0]
        if subscription.status != SubscriptionStatus.ACTIVE:
            return 404, ErrorOut(message="アクティブなサブスクリプションが見つかりません")

        payment = injector.get(PaymentInterface)
        result = payment.cancel_subscription(subscription.external_id)
        match result:
            case CancelSuccess(canceled_at=canceled_at, period_end=period_end):
                updated = replace(subscription, canceled_at=canceled_at, current_period_end=period_end)
                sub_repo.bulk_save([updated])
                log.info("PaymentAPI cancel succeeded", user_id=user_id, external_id=subscription.external_id)
                return 200, PaymentCancelOut(canceled_at=canceled_at, period_end=period_end)
            case CancelFailed(error=error, message=message):
                log.error("Payment cancel failed", error=error.value, message=message)
                return 500, ErrorOut(message="解約処理に失敗しました")
