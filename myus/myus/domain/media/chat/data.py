from dataclasses import dataclass
from datetime import date, datetime
from myus.domain.channel.data import ChannelData
from myus.domain.hashtag.data import HashtagData


@dataclass(frozen=True, slots=True)
class ChatData:
    id: int
    ulid: str
    title: str
    content: str
    read: int
    like: int
    period: date
    publish: bool
    publish_at: datetime
    created: datetime
    updated: datetime
    thread_count: int
    joined_count: int
    category_ulid: str
    channel: ChannelData
    hashtags: list[HashtagData]
