from dataclasses import dataclass
from datetime import datetime
from myus.domain.media.audio.data import AudioData
from .user import AuthorDTO


@dataclass(frozen=True, slots=True)
class PlaylistDTO:
    ulid: str
    title: str
    image: str
    publish: bool
    count: int
    audio_ulids: list[str]
    updated: datetime


@dataclass(frozen=True, slots=True)
class PlaylistDetailDTO:
    ulid: str
    title: str
    description: str
    image: str
    thumbnail_audio_ulid: str
    publish: bool
    is_owner: bool
    updated: datetime
    author: AuthorDTO
    audios: list[AudioData]


@dataclass(frozen=True, slots=True)
class PlaylistCreateDTO:
    title: str
    publish: bool
    audio_ulid: str


@dataclass(frozen=True, slots=True)
class PlaylistUpdateDTO:
    title: str
    description: str
    thumbnail_audio_ulid: str
    publish: bool
    audio_ulids: list[str]
