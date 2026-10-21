from typing import assert_never
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.adapter.auth import auth_check
from api.src.domain.interface.payment.provider.data import CancelFailed, CancelSuccess, CheckoutCreated, CheckoutFailed, WebhookVerified, WebhookVerifyFailed
from api.src.types.schema.common import ErrorOut, ErrorType
from api.src.types.schema.payment import PaymentCancelOut, PaymentCheckoutIn, PaymentCheckoutOut, PaymentWebhookOut
from api.src.usecase.payment import cancel_subscription, create_checkout, receive_webhook_inbox, verify_webhook
from api.utils.common.result import FatalError, NotFoundError
from api.utils.enum.payment import WebhookVerifyError


class PaymentAPI:
    """料金プランAPI"""

    router = Router()

    @staticmethod
    @router.post("/checkout", response={200: PaymentCheckoutOut, 400: ErrorOut, 500: ErrorOut})
    def checkout(request: HttpRequest, input: PaymentCheckoutIn):
        log.info("PaymentAPI checkout", plan=input.plan)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        checkout_ret = create_checkout(user_id, input.plan)
        if checkout_ret.is_err:
            message = checkout_ret.err_value.message
            match checkout_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(checkout_ret.err_value)

        checkout = checkout_ret.ok_value
        match checkout:
            case CheckoutCreated(session=session):
                return 200, PaymentCheckoutOut(url=session.redirect_url)
            case CheckoutFailed(error=error, message=message):
                log.error("Payment checkout failed", error=error.value, message=message)
                return 500, ErrorOut(type=ErrorType.INTERNAL, message="error.checkoutFailed")

    @staticmethod
    @router.post("/webhook", response={200: PaymentWebhookOut, 400: ErrorOut, 500: ErrorOut})
    def webhook(request: HttpRequest):
        payload = request.body
        signature = request.META.get("HTTP_STRIPE_SIGNATURE", "")

        verify_ret = verify_webhook(payload, signature)
        if verify_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        verification = verify_ret.ok_value
        match verification:
            case WebhookVerifyFailed(error=WebhookVerifyError.UNSUPPORTED_EVENT, message=message):
                log.info("PaymentAPI webhook unsupported event", message=message)
                return 200, PaymentWebhookOut(message="Unsupported event type")
            case WebhookVerifyFailed(error=error, message=message):
                log.warning("PaymentAPI webhook verify failed", error=error.value, message=message)
                return 400, ErrorOut(type=ErrorType.VALIDATION, message="Invalid webhook")
            case WebhookVerified(event=event):
                log.info("PaymentAPI webhook verified", event_id=event.event_id, event_type=event.event_type.value)

                receive_ret = receive_webhook_inbox(event)
                if receive_ret.is_err:
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

                is_received = receive_ret.ok_value
                if not is_received:
                    return 200, PaymentWebhookOut(message="Already processed")

                return 200, PaymentWebhookOut(message="OK")

    @staticmethod
    @router.post("/cancel", response={200: PaymentCancelOut, 400: ErrorOut, 500: ErrorOut})
    def cancel(request: HttpRequest):
        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        cancel_ret = cancel_subscription(user_id)
        if cancel_ret.is_err:
            message = cancel_ret.err_value.message
            match cancel_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(cancel_ret.err_value)

        cancellation = cancel_ret.ok_value
        match cancellation:
            case CancelSuccess(canceled_at=canceled_at, period_end=period_end):
                return 200, PaymentCancelOut(canceled_at=canceled_at, period_end=period_end)
            case CancelFailed(error=error, message=message):
                log.error("Payment cancel failed", error=error.value, message=message)
                return 500, ErrorOut(type=ErrorType.INTERNAL, message="error.cancelFailed")
