from dataclasses import dataclass
from datetime import datetime
from api.src.types.data.user import AuthorData


@dataclass(frozen=True, slots=True)
class ReplyData:
    ulid: str
    text: str
    created: datetime
    updated: datetime
    is_comment_like: bool
    like_count: int
    author: AuthorData


@dataclass(frozen=True, slots=True)
class CommentData:
    id: int
    ulid: str
    author_id: int
    parent_id: int | None
    type_no: int
    type_name: str
    object_id: int
    text: str
    created: datetime
    updated: datetime
    is_comment_like: bool
    like_count: int
    author: AuthorData
    replys: list[ReplyData]
