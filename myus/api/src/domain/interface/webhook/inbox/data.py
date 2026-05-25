from dataclasses import dataclass
from datetime import datetime
from api.utils.enum.payment import PaymentProvider, WebhookEventType


@dataclass(frozen=True, slots=True)
class WebhookInboxData:
    id: int
    provider: PaymentProvider
    event_id: str
    event_type: WebhookEventType
    external_id: str
    occurred_at: datetime
