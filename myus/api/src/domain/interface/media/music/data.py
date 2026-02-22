from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.media.data import HashtagData


@dataclass(frozen=True, slots=True)
class MusicData:
    id: int
    ulid: str
    title: str
    content: str
    lyric: str
    music: str
    read: int
    like: int
    download: bool
    publish: bool
    created: datetime
    updated: datetime
    comment_count: int
    channel: ChannelData
    hashtags: list[HashtagData]
