import stripe
from django.conf import settings
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.payment import PaymentCheckoutIn, PaymentCheckoutOut
from api.src.usecase.auth import auth_check
from api.src.usecase.user import get_user_data


class PaymentAPI:
    """料金プランAPI"""

    router = Router()

    @staticmethod
    @router.post("/checkout", response={200: PaymentCheckoutOut, 401: ErrorOut, 404: ErrorOut, 500: ErrorOut})
    def checkout(request: HttpRequest, input: PaymentCheckoutIn):
        log.info("PaymentAPI checkout", stripe_id=input.stripe_id)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        user_data = get_user_data(user_id=user_id)
        if user_data is None:
            return 404, ErrorOut(message="Not Found")

        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.create(
                mode="subscription",
                line_items=[{"price": input.stripe_id, "quantity": 1}],
                success_url=f"{settings.FRONTEND_URL}/setting/payment/success",
                cancel_url=f"{settings.FRONTEND_URL}/setting/payment",
                customer_email=user_data.user.email,
            )
        except stripe.StripeError as e:
            log.error("Stripe checkout error", exc=e)
            return 500, ErrorOut(message="決済セッションの作成に失敗しました!")

        if session.url is None:
            log.error("Stripe checkout url is None")
            return 500, ErrorOut(message="決済セッションの作成に失敗しました!")

        return 200, PaymentCheckoutOut(url=session.url)
