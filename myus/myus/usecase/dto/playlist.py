from dataclasses import dataclass
from datetime import datetime
from myus.domain.media.music.data import MusicData
from .user import AuthorDTO


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
    description: str
    image: str
    thumbnail_music_ulid: str
    publish: bool
    is_owner: bool
    updated: datetime
    author: AuthorDTO
    musics: list[MusicData]


@dataclass(frozen=True, slots=True)
class PlaylistCreateDTO:
    title: str
    publish: bool
    music_ulid: str


@dataclass(frozen=True, slots=True)
class PlaylistUpdateDTO:
    title: str
    description: str
    thumbnail_music_ulid: str
    publish: bool
    music_ulids: list[str]
