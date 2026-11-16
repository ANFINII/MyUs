from dataclasses import dataclass
from datetime import datetime
from myus.domain.media.music.data import MusicData


@dataclass(frozen=True, slots=True)
class PlaylistDTO:
    ulid: str
    title: str
    publish: bool
    count: int
    image: str
    music_ulids: list[str]
    updated: datetime


@dataclass(frozen=True, slots=True)
class PlaylistDetailDTO:
    ulid: str
    title: str
    publish: bool
    is_owner: bool
    author_ulid: str
    author_avatar: str
    author_nickname: str
    musics: list[MusicData]
    updated: datetime


@dataclass(frozen=True, slots=True)
class PlaylistCreateDTO:
    title: str
    publish: bool
    music_ulid: str


@dataclass(frozen=True, slots=True)
class PlaylistUpdateDTO:
    title: str
    publish: bool
    music_ulids: list[str]
