from dataclasses import dataclass
from datetime import datetime
from myus.utils.enum.media import CommentType
from .user import AuthorDTO


@dataclass(frozen=True, slots=True)
class ReplyDTO:
    ulid: str
    text: str
    created: datetime
    updated: datetime
    is_comment_like: bool
    like_count: int
    author: AuthorDTO


@dataclass(frozen=True, slots=True)
class CommentDTO:
    ulid: str
    text: str
    created: datetime
    updated: datetime
    is_comment_like: bool
    like_count: int
    author: AuthorDTO
    replys: list[ReplyDTO]


@dataclass(frozen=True, slots=True)
class CommentCreateDTO:
    text: str
    type_name: CommentType
    object_ulid: str
    parent_ulid: str | None
