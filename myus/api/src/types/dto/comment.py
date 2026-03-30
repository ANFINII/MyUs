from dataclasses import dataclass
from datetime import datetime
from api.src.types.dto.user import AuthorDTO


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
