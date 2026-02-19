from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.channel.data import ChannelData


@dataclass(frozen=True, slots=True)
class MusicData:
    id: int
    ulid: str
    title: str
    content: str
    lyric: str
    music: str
    read: int
    download: bool
    publish: bool
    created: datetime
    updated: datetime
    like_count: int
    comment_count: int
    channel: ChannelData
