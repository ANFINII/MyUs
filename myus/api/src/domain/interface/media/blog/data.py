from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BlogData:
    id: int
    ulid: str
    channel_id: int
    title: str
    content: str
    richtext: str
    delta: str
    image: str
    read: int
    publish: bool
