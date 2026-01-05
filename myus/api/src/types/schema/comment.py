from datetime import datetime
from pydantic import BaseModel
from api.src.types.schema.user import AuthorOut
from api.utils.enum.index import CommentTypeNo, CommentType


class CommentListIn(BaseModel):
    type_no: CommentTypeNo
    object_id: int


class CommentCreateIn(BaseModel):
    text: str
    type_no: CommentTypeNo
    type_name: CommentType
    object_ulid: str
    parent_ulid: str | None


class CommentUpdateIn(BaseModel):
    text: str


class ReplyOut(BaseModel):
    id: int
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
