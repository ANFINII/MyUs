from datetime import datetime
from dataclasses import dataclass
from api.types.data.user import AuthorData
from api.utils.enum.index import CommentTypeNo, CommentType


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
    author: AuthorData
    text: str
    type_name: CommentType
    type_no: CommentTypeNo
    object_id: int
    parent_id: int | None
