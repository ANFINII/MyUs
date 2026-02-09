from dataclasses import dataclass
from datetime import datetime


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
    owner_id: int
    created: datetime
    updated: datetime
    like_count: int
    comment_count: int
