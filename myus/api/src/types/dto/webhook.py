from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WebhookOutboxPayloadDTO:
    provider: str
    event_id: str
    event_type: str
    external_id: str
    occurred_at: str
