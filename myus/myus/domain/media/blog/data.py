from dataclasses import dataclass
from datetime import datetime
from myus.domain.channel.data import ChannelData
from myus.domain.hashtag.data import HashtagData


@dataclass(frozen=True, slots=True)
class BlogData:
    id: int
    ulid: str
    title: str
    content: str
    richtext: str
    image: str
    read: int
    like: int
    publish: bool
    publish_at: datetime
    is_promotion: bool
    created: datetime
    updated: datetime
    category_ulid: str
    channel: ChannelData
    hashtags: list[HashtagData]
