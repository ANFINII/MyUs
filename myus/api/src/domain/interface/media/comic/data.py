from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.channel.data import ChannelData


@dataclass(frozen=True, slots=True)
class ComicData:
    id: int
    ulid: str
    title: str
    content: str
    image: str
    read: int
    publish: bool
    created: datetime
    updated: datetime
    like_count: int
    comment_count: int
    channel: ChannelData
