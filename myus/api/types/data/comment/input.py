from typing import Optional
from ninja import Schema
from api.utils.enum.index import CommentTypeNo, CommentType


class CommentListInData(Schema):
    type_no: CommentTypeNo
    object_id: int


class CommentCreateInData(Schema):
    text: str
    type_no: CommentTypeNo
    type_name: CommentType
    object_ulid: str
    parent_ulid: str | None = None


class CommentUpdateInData(Schema):
    text: str
