from dataclasses import dataclass


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
