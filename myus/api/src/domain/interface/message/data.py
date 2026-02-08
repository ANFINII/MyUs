from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MessageData:
    id: int
    ulid: str
    author_id: int
    chat_id: int
    parent_id: int | None
    text: str
    delta: str
