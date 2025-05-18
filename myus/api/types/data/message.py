from datetime import datetime
from dataclasses import dataclass
from api.types.data.user import AuthorData


@dataclass(frozen=True, slots=True)
class MessageReplyData:
    id: int
    parent_id: int
    text: str
    created: datetime
    updated: datetime
    author: AuthorData


@dataclass(frozen=True, slots=True)
class MessageData:
    id: int
    text: str
    created: datetime
    updated: datetime
    author: AuthorData
