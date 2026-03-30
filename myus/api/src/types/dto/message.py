from dataclasses import dataclass
from datetime import datetime
from api.src.types.dto.user import AuthorData


@dataclass(frozen=True, slots=True)
class MessageReplyData:
    ulid: str
    parent_id: str
    text: str
    created: datetime
    updated: datetime
    author: AuthorData


@dataclass(frozen=True, slots=True)
class MessageData:
    ulid: str
    text: str
    reply_count: int
    created: datetime
    updated: datetime
    author: AuthorData
