from datetime import datetime
from dataclasses import dataclass
from api.src.types.data.user import AuthorData
from api.utils.enum.index import CommentTypeNo, CommentType


@dataclass(frozen=True, slots=True)
class ReplyData:
    id: int
    text: str
    created: datetime
    updated: datetime
    is_comment_like: bool
    like_count: int
    author: AuthorData


@dataclass(frozen=True, slots=True)
class CommentData:
    ulid: str
    text: str
    created: datetime
    updated: datetime
    is_comment_like: bool
    like_count: int
    author: AuthorData
    replys: list[ReplyData]


@dataclass(frozen=True, slots=True)
class CommentCreateData:
    author_id: int
    text: str
    type_no: CommentTypeNo
    type_name: CommentType
    object_id: int
    parent_id: int | None
