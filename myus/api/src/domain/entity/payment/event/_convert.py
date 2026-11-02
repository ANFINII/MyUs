from api.db.models.payment import PaymentEvent
from api.src.domain.interface.payment.event.data import PaymentEventData
from api.utils.enum.payment import PaymentProvider, WebhookEventType


def convert_data(obj: PaymentEvent) -> PaymentEventData:
    return PaymentEventData(
        id=obj.id,
        provider=PaymentProvider(obj.provider),
        event_id=obj.event_id,
        event_type=WebhookEventType(obj.event_type),
        external_id=obj.external_id,
        payload=obj.payload,
        occurred_at=obj.occurred_at,
    )


def marshal_data(data: PaymentEventData) -> PaymentEvent:
    return PaymentEvent(
        id=data.id if data.id != 0 else None,
        provider=data.provider,
        event_id=data.event_id,
        event_type=data.event_type,
        external_id=data.external_id,
        payload=data.payload,
        occurred_at=data.occurred_at,
    )
