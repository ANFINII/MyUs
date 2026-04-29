from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.hashtag.data import HashtagData


@dataclass(frozen=True, slots=True)
class ComicData:
    id: int
    ulid: str
    title: str
    content: str
    image: str
    pages: list[str]
    read: int
    like: int
    publish: bool
    created: datetime
    updated: datetime
    category_ulid: str
    channel: ChannelData
    hashtags: list[HashtagData]
