from datetime import datetime
from dataclasses import dataclass
from api.types.data.user import AuthorData


@dataclass(frozen=True, slots=True)
class ReplyData:
    id: int
    text: str
    created: datetime
    updated: datetime
    author: AuthorData


@dataclass(frozen=True, slots=True)
class CommentData:
    id: int
    text: str
    created: datetime
    updated: datetime
    replys: list[ReplyData]
    author: AuthorData


@dataclass(frozen=True, slots=True)
class CommentInData:
    text: str
    type: str
