import stripe
from datetime import datetime, timezone
from typing import assert_never
from django.conf import settings
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
    SessionCreateParamsLineItemPriceData,
    SessionCreateParamsLineItemPriceDataProductData,
    SessionCreateParamsPaymentIntentData,
    SessionCreateParamsPaymentIntentDataTransferData,
    SessionCreateParamsSubscriptionData,
    SessionCreateParamsSubscriptionDataTransferData,
)
from api.src.adapter.external.payment.stripe._type import stripe_event_type
from api.src.domain.interface.payment.data import Money
from api.src.domain.interface.payment.provider.data import CheckoutData, CheckoutFailed, WebhookVerifyFailed
from api.src.domain.interface.payment.webhook_inbox.data import WebhookInboxData
from api.utils.enum.i18n import Locale
from api.utils.enum.payment import CheckoutError, PaymentProvider, PaymentType, WebhookVerifyError
from api.utils.enum.user import PlanName


def convert_stripe_event(event: stripe.Event) -> WebhookInboxData | WebhookVerifyFailed:
    event_type = stripe_event_type(event.type)
    if event_type is None:
        return WebhookVerifyFailed(error=WebhookVerifyError.UNSUPPORTED_EVENT, message=f"unsupported event_type={event.type}")

    external_id: str = getattr(event.data.object, "id", "")
    return WebhookInboxData(
        id=0,
        provider=PaymentProvider.STRIPE,
        event_id=event.id,
        event_type=event_type,
        external_id=external_id,
        occurred_at=datetime.fromtimestamp(event.created, tz=timezone.utc),
    )


def stripe_price_id(product_code: str) -> str:
    mapping: dict[str, str] = {
        PlanName.BASIC: settings.STRIPE_PRICE_ID_BASIC,
        PlanName.STANDARD: settings.STRIPE_PRICE_ID_STANDARD,
        PlanName.PREMIUM: settings.STRIPE_PRICE_ID_PREMIUM,
        PlanName.ULTIMATE: settings.STRIPE_PRICE_ID_ULTIMATE,
    }
    return mapping.get(product_code, "")


def stripe_locale(locale: Locale) -> str:
    match locale:
        case Locale.JA:
            return "ja"
        case Locale.EN:
            return "en"
        case Locale.ZH:
            return "zh"
        case Locale.KO:
            return "ko"
        case _:
            assert_never(locale)


def stripe_mode(payment_type: PaymentType) -> str:
    match payment_type:
        case PaymentType.SUBSCRIPTION:
            return "subscription"
        case PaymentType.ONE_TIME:
            return "payment"
        case _:
            assert_never(payment_type)


def fee_percent(fee: Money, price: Money) -> int:
    if price.amount <= 0:
        return 0
    return int(fee.amount * 100 / price.amount)


def convert_line_items(input: CheckoutData) -> list[SessionCreateParamsLineItem] | CheckoutFailed:
    match input.payment_type:
        case PaymentType.SUBSCRIPTION:
            price_id = stripe_price_id(input.product_code)
            if len(price_id) == 0:
                return CheckoutFailed(error=CheckoutError.UNKNOWN_PRODUCT, message=f"price_id not configured for product_code={input.product_code}")
            return [SessionCreateParamsLineItem(price=price_id, quantity=1)]
        case PaymentType.ONE_TIME:
            if input.price.amount <= 0:
                return CheckoutFailed(error=CheckoutError.INVALID_AMOUNT, message=f"invalid amount={input.price.amount}")
            price_data = SessionCreateParamsLineItemPriceData(
                currency=input.price.currency.value.lower(),
                unit_amount=input.price.amount,
                product_data=SessionCreateParamsLineItemPriceDataProductData(name=input.description),
            )
            return [SessionCreateParamsLineItem(price_data=price_data, quantity=1)]
        case _:
            assert_never(input.payment_type)


def convert_marketplace_params(input: CheckoutData) -> SessionCreateParams:
    if len(input.marketplace.seller_id) == 0:
        return SessionCreateParams()

    match input.payment_type:
        case PaymentType.SUBSCRIPTION:
            sub_transfer = SessionCreateParamsSubscriptionDataTransferData(destination=input.marketplace.seller_id)
            sub_data = SessionCreateParamsSubscriptionData(transfer_data=sub_transfer)
            pct = fee_percent(input.marketplace.application_fee, input.price)
            if pct > 0:
                sub_data["application_fee_percent"] = pct
            return SessionCreateParams(subscription_data=sub_data)
        case PaymentType.ONE_TIME:
            pi_transfer = SessionCreateParamsPaymentIntentDataTransferData(destination=input.marketplace.seller_id)
            pi_data = SessionCreateParamsPaymentIntentData(transfer_data=pi_transfer)
            if input.marketplace.application_fee.amount > 0:
                pi_data["application_fee_amount"] = input.marketplace.application_fee.amount
            return SessionCreateParams(payment_intent_data=pi_data)
        case _:
            assert_never(input.payment_type)


def convert_stripe_params(input: CheckoutData) -> SessionCreateParams | CheckoutFailed:
    line_items = convert_line_items(input)
    if isinstance(line_items, CheckoutFailed):
        return line_items

    return SessionCreateParams(
        mode=stripe_mode(input.payment_type),
        line_items=line_items,
        success_url=input.redirect.success_url,
        cancel_url=input.redirect.cancel_url,
        customer_email=input.customer.email,
        locale=stripe_locale(input.locale),
        **convert_marketplace_params(input),
    )
