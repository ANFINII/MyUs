from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class MusicData:
    id: int
    ulid: str
    channel_id: int
    title: str
    content: str
    lyric: str
    music: str
    read: int
    download: bool
    publish: bool
    owner_id: int = 0
    created: datetime = datetime.min
    updated: datetime = datetime.min
    like_count: int = 0
    comment_count: int = 0
