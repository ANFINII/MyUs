from django.conf import settings
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.domain.interface.payment.data import CheckoutCreated, CheckoutData, CheckoutFailed, CustomerData, MarketplaceData, Money, RedirectUrls
from api.src.domain.interface.payment.interface import PaymentInterface
from api.src.injectors.container import injector
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.payment import PaymentCheckoutIn, PaymentCheckoutOut
from api.src.usecase.auth import auth_check
from api.src.usecase.user import get_user_data
from api.utils.enum.i18n import Currency, Locale
from api.utils.enum.payment import PaymentType
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
