from dataclasses import dataclass
from datetime import datetime
from api.utils.enum.payment import PaymentProvider, WebhookEventType


@dataclass(frozen=True, slots=True)
class PaymentEventData:
    id: int
    provider: PaymentProvider
    event_id: str
    event_type: WebhookEventType
    external_id: str
    payload: str
    occurred_at: datetime
