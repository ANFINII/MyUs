from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class EventEnvelope[E]:
    event_id: UUID
    aggregate_type: str
    aggregate_id: str
    seq: int
    occurred_at: datetime
    event: E
