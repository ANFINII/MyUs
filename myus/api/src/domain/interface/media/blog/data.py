from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.hashtag.data import HashtagData


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
    channel: ChannelData
    category_ulid: str
    hashtags: list[HashtagData]
