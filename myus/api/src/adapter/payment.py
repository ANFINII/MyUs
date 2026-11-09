from datetime import datetime, timezone
from typing import assert_never
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.adapter.auth import auth_check
from api.src.domain.interface.payment.provider.data import CancelFailed, CancelSuccess, CheckoutCreated, CheckoutFailed, PlanChangeFailed, PlanChangeSuccess, RevokeFailed, RevokeSuccess, WebhookVerified, WebhookVerifyFailed
from api.src.types.schema.common import ErrorOut, ErrorType
from api.src.types.schema.payment import PaymentCancelOut, PaymentChangeIn, PaymentCheckoutIn, PaymentCheckoutOut, PaymentSubscriptionOut, PaymentWebhookOut
from api.src.usecase.payment.core import cancel_subscription, change_plan, create_checkout, get_subscription, receive_payment_event, revoke_cancellation, verify_webhook
from api.utils.common.result import FatalError, NotFoundError, ValidationError
from api.utils.enum.payment import PaymentProvider, WebhookVerifyError


class PaymentAPI:
    """料金プランAPI"""

    router = Router()

    @staticmethod
    @router.get("/subscription", response={200: PaymentSubscriptionOut, 400: ErrorOut, 500: ErrorOut})
    def subscription(request: HttpRequest):
        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        subscription_ret = get_subscription(user_id)
        if subscription_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        subscription = subscription_ret.ok_value
        if subscription is None:
            return 200, PaymentSubscriptionOut(is_canceled=False, period_end=datetime.min.replace(tzinfo=timezone.utc))

        is_canceled = subscription.canceled_at != datetime.min.replace(tzinfo=timezone.utc)
        return 200, PaymentSubscriptionOut(is_canceled=is_canceled, period_end=subscription.current_period_end)

    @staticmethod
    @router.post("/checkout", response={200: PaymentCheckoutOut, 400: ErrorOut, 500: ErrorOut})
    def checkout(request: HttpRequest, input: PaymentCheckoutIn):
        log.info("PaymentAPI checkout", plan=input.plan, locale=input.locale.value)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        checkout_ret = create_checkout(user_id, input.plan, input.locale)
        if checkout_ret.is_err:
            message = checkout_ret.err_value.message
            match checkout_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
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

        verify_ret = verify_webhook(PaymentProvider.STRIPE, payload, signature)
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

                receive_ret = receive_payment_event(event)
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

    @staticmethod
    @router.post("/cancel/revoke", response={200: None, 400: ErrorOut, 500: ErrorOut})
    def revoke(request: HttpRequest):
        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        revoke_ret = revoke_cancellation(user_id)
        if revoke_ret.is_err:
            message = revoke_ret.err_value.message
            match revoke_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(revoke_ret.err_value)

        revoke = revoke_ret.ok_value
        match revoke:
            case RevokeSuccess():
                return 200, None
            case RevokeFailed(error=error, message=message):
                log.error("Payment cancel revoke failed", error=error.value, message=message)
                return 500, ErrorOut(type=ErrorType.INTERNAL, message="error.cancellationRevokeFailed")

    @staticmethod
    @router.post("/change", response={200: None, 400: ErrorOut, 500: ErrorOut})
    def change(request: HttpRequest, input: PaymentChangeIn):
        log.info("PaymentAPI change", plan=input.plan)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        change_ret = change_plan(user_id, input.plan)
        if change_ret.is_err:
            message = change_ret.err_value.message
            match change_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(change_ret.err_value)

        change = change_ret.ok_value
        match change:
            case PlanChangeSuccess():
                return 200, None
            case PlanChangeFailed(error=error, message=message):
                log.error("Payment plan change failed", error=error.value, message=message)
                return 500, ErrorOut(type=ErrorType.INTERNAL, message="error.planChangeFailed")
