from dataclasses import dataclass
from datetime import datetime
from api.utils.enum.payment import PaymentProvider, WebhookEventType, WebhookDeliveryStatus


@dataclass(frozen=True, slots=True)
class WebhookOutboxData:
    id: int
    provider: PaymentProvider
    event_type: WebhookEventType
    external_id: str
    payload: str
    status: WebhookDeliveryStatus
    occurred_at: datetime
    delivered_at: datetime
