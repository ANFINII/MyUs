from dataclasses import dataclass
from datetime import date, datetime


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
    owner_id: int = 0
    created: datetime = datetime.min
    updated: datetime = datetime.min
    like_count: int = 0
    thread_count: int = 0
    joined_count: int = 0
