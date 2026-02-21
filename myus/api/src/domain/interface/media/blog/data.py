from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.channel.data import ChannelData


@dataclass(frozen=True, slots=True)
class BlogData:
    id: int
    ulid: str
    title: str
    content: str
    richtext: str
    delta: str
    image: str
    read: int
    like: int
    publish: bool
    created: datetime
    updated: datetime
    comment_count: int
    channel: ChannelData
