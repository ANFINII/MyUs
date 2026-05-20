from api.db.models.payment import WebhookEvent
from api.src.domain.interface.payment.data import WebhookEventData
from api.utils.enum.payment import PaymentProvider, WebhookEventType


def convert_data(obj: WebhookEvent) -> WebhookEventData:
    return WebhookEventData(
        id=obj.id,
        provider=PaymentProvider(obj.provider),
        event_id=obj.event_id,
        event_type=WebhookEventType(obj.event_type),
        external_id=obj.external_id,
        occurred_at=obj.occurred_at,
    )


def marshal_data(data: WebhookEventData) -> WebhookEvent:
    return WebhookEvent(
        id=data.id if data.id != 0 else None,
        provider=data.provider,
        event_id=data.event_id,
        event_type=data.event_type,
        external_id=data.external_id,
        occurred_at=data.occurred_at,
    )
