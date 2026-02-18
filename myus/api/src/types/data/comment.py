from dataclasses import dataclass
from api.utils.enum.index import CommentType, CommentTypeNo


@dataclass(frozen=True, slots=True)
class CommentCreateData:
    author_id: int
    text: str
    type_no: CommentTypeNo
    type_name: CommentType
    object_id: int
    parent_id: int | None
