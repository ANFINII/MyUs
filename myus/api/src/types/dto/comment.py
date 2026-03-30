from dataclasses import dataclass
from datetime import datetime
from api.src.types.dto.user import AuthorDTO
from api.utils.enum.index import CommentType, CommentTypeNo


@dataclass(frozen=True, slots=True)
class CommentCreateDTO:
    author_id: int
    text: str
    type_no: CommentTypeNo
    type_name: CommentType
    object_id: int
    parent_id: int | None


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
class CommentGetDTO:
    ulid: str
    text: str
    created: datetime
    updated: datetime
    is_comment_like: bool
    like_count: int
    author: AuthorDTO
    replys: list[ReplyDTO]
