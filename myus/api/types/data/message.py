from datetime import datetime
from dataclasses import dataclass
from api.types.data.user import AuthorData


@dataclass(frozen=True, slots=True)
class ReplyData:
    id: str
    text: str
    created: datetime
    updated: datetime
    author: AuthorData


@dataclass(frozen=True, slots=True)
class MessageData:
    id: str
    text: str
    created: datetime
    updated: datetime
    replys: list[ReplyData]
    author: AuthorData


@dataclass(frozen=True, slots=True)
class CommentInData:
    text: str
    type: str
