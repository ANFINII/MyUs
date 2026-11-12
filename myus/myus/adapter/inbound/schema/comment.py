from datetime import datetime
from pydantic import BaseModel
from myus.utils.enum.media import CommentType
from .user import AuthorOut


class CommentCreateIn(BaseModel):
    text: str
    type_name: CommentType
    object_ulid: str
    parent_ulid: str | None = None


class CommentUpdateIn(BaseModel):
    text: str


class ReplyOut(BaseModel):
    ulid: str
    text: str
    created: datetime
    updated: datetime
    is_comment_like: bool
    like_count: int
    author: AuthorOut


class CommentOut(BaseModel):
    ulid: str
    text: str
    created: datetime
    updated: datetime
    is_comment_like: bool
    like_count: int
    author: AuthorOut
    replys: list[ReplyOut]
