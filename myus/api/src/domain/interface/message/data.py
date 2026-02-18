from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class MessageData:
    id: int
    ulid: str
    author_id: int
    chat_id: int
    parent_id: int | None
    parent_ulid: str
    text: str
    delta: str
    created: datetime
    updated: datetime
