from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.channel.data import ChannelData


@dataclass(frozen=True, slots=True)
class VideoData:
    id: int
    ulid: str
    title: str
    content: str
    image: str
    video: str
    convert: str
    read: int
    like: int
    publish: bool
    created: datetime
    updated: datetime
    comment_count: int
    channel: ChannelData
