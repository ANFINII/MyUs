from api.db.models.payment import WebhookOutbox
from api.src.domain.interface.webhook.outbox.data import WebhookOutboxData
from api.utils.enum.payment import PaymentProvider, WebhookEventType, WebhookDeliveryStatus


def convert_data(obj: WebhookOutbox) -> WebhookOutboxData:
    return WebhookOutboxData(
        id=obj.id,
        provider=PaymentProvider(obj.provider),
        event_type=WebhookEventType(obj.event_type),
        external_id=obj.external_id,
        payload=obj.payload,
        status=WebhookDeliveryStatus(obj.status),
        occurred_at=obj.occurred_at,
        delivered_at=obj.delivered_at,
    )


def marshal_data(data: WebhookOutboxData) -> WebhookOutbox:
    return WebhookOutbox(
        id=data.id if data.id != 0 else None,
        provider=data.provider,
        event_type=data.event_type,
        external_id=data.external_id,
        payload=data.payload,
        status=data.status,
        occurred_at=data.occurred_at,
        delivered_at=data.delivered_at,
    )
