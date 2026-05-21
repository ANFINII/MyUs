from django.conf import settings
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.domain.interface.payment.data import CheckoutCreated, CheckoutData, CheckoutFailed, CustomerData, MarketplaceData, Money, RedirectUrls, WebhookVerified, WebhookVerifyFailed
from api.src.domain.interface.payment.interface import PaymentInterface
from api.src.domain.interface.payment.webhook_event.interface import FilterOption, SortOption, WebhookEventInterface
from api.src.injectors.container import injector
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.payment import PaymentCheckoutIn, PaymentCheckoutOut, PaymentWebhookOut
from api.src.usecase.auth import auth_check
from api.src.usecase.user import get_user_data
from api.utils.enum.i18n import Currency, Locale
from api.utils.enum.payment import PaymentType, WebhookVerifyError
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

                webhook_event_repo = injector.get(WebhookEventInterface)
                existing_ids = webhook_event_repo.get_ids(
                    FilterOption(provider=event.provider.value, event_id=event.event_id),
                    SortOption(),
                    limit=1,
                )
                if len(existing_ids) > 0:
                    log.info("PaymentAPI webhook already processed", event_id=event.event_id)
                    return 200, PaymentWebhookOut(message="Already processed")

                webhook_event_repo.bulk_save([event])
                return 200, PaymentWebhookOut(message="OK")
