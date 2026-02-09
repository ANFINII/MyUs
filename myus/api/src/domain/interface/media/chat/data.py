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
    owner_id: int
    created: datetime
    updated: datetime
    like_count: int
    thread_count: int
    joined_count: int
