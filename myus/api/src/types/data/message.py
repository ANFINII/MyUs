from datetime import datetime
from dataclasses import dataclass
from api.src.types.data.user import AuthorData


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
    created: datetime
    updated: datetime
    author: AuthorData
