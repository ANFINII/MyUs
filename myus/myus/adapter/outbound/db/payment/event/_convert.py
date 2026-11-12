from typing import assert_never
from pydantic import TypeAdapter
from myus.db.models.payment import PaymentEvent
from myus.domain.payment.event.data import PaymentEventContent, PaymentEventData, PaymentFailedContent, PaymentPaidContent, PayoutContent, ProviderSubscriptionData, RefundContent
from myus.utils.enum.payment import PaymentProvider, WebhookEventType


def convert_data(obj: PaymentEvent) -> PaymentEventData:
    event_type = WebhookEventType(obj.event_type)
    return PaymentEventData(
        id=obj.id,
        provider=PaymentProvider(obj.provider),
        event_id=obj.event_id,
        event_type=event_type,
        external_id=obj.external_id,
        payload=obj.payload,
        content=convert_content(event_type, obj.content),
        occurred_at=obj.occurred_at,
        processed_at=obj.processed_at,
        attempts=obj.attempts,
        last_error=obj.last_error,
    )


def convert_content(event_type: WebhookEventType, content: str) -> PaymentEventContent:
    match event_type:
        case WebhookEventType.SUBSCRIPTION_CREATED | WebhookEventType.SUBSCRIPTION_UPDATED | WebhookEventType.SUBSCRIPTION_CANCELED:
            return TypeAdapter(ProviderSubscriptionData).validate_json(content)
        case WebhookEventType.PAYMENT_SUCCEEDED:
            return TypeAdapter(PaymentPaidContent).validate_json(content)
        case WebhookEventType.PAYMENT_FAILED:
            return TypeAdapter(PaymentFailedContent).validate_json(content)
        case WebhookEventType.REFUND_ISSUED:
            return TypeAdapter(RefundContent).validate_json(content)
        case WebhookEventType.PAYOUT_PAID:
            return TypeAdapter(PayoutContent).validate_json(content)
        case _:
            assert_never(event_type)


def marshal_data(data: PaymentEventData) -> PaymentEvent:
    return PaymentEvent(
        id=data.id if data.id != 0 else None,
        provider=data.provider,
        event_id=data.event_id,
        event_type=data.event_type,
        external_id=data.external_id,
        payload=data.payload,
        content=marshal_content(data.content),
        occurred_at=data.occurred_at,
        processed_at=data.processed_at,
        attempts=data.attempts,
        last_error=data.last_error,
    )


def marshal_content(content: PaymentEventContent) -> str:
    return TypeAdapter(PaymentEventContent).dump_json(content).decode()
