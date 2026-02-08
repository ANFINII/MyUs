from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class ChatData:
    id: int
    ulid: str
    channel_id: int
    title: str
    content: str
    read: int
    period: date
    publish: bool
