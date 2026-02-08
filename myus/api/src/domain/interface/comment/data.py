from dataclasses import dataclass


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
    deleted: bool
