from dataclasses import dataclass
from datetime import datetime
from myus.domain.channel.data import ChannelData
from myus.domain.hashtag.data import HashtagData


@dataclass(frozen=True, slots=True)
class PictureData:
    id: int
    ulid: str
    title: str
    content: str
    image: str
    read: int
    like: int
    publish: bool
    publish_at: datetime
    created: datetime
    updated: datetime
    category_ulid: str
    channel: ChannelData
    hashtags: list[HashtagData]
