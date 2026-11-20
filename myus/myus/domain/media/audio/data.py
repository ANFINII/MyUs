from dataclasses import dataclass
from datetime import datetime
from ...channel.data import ChannelData
from ...hashtag.data import HashtagData


@dataclass(frozen=True, slots=True)
class AudioData:
    id: int
    ulid: str
    title: str
    content: str
    lyric: str
    image: str
    audio: str
    gain: float
    read: int
    like: int
    publish: bool
    publish_at: datetime
    created: datetime
    updated: datetime
    category_ulid: str
    channel: ChannelData
    hashtags: list[HashtagData]
