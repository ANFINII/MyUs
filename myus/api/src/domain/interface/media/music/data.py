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
    owner_id: int
    created: datetime
    updated: datetime
    like_count: int
    comment_count: int
