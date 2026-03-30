from dataclasses import dataclass
from datetime import datetime
from api.src.types.dto.user import AuthorDTO


@dataclass(frozen=True, slots=True)
class MessageReplyDTO:
    ulid: str
    parent_id: str
    text: str
    created: datetime
    updated: datetime
    author: AuthorDTO


@dataclass(frozen=True, slots=True)
class MessageDTO:
    ulid: str
    text: str
    reply_count: int
    created: datetime
    updated: datetime
    author: AuthorDTO
