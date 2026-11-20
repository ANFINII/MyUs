from datetime import datetime
from pydantic import BaseModel
from .media.output import AudioOut
from .user import AuthorOut


class PlaylistIn(BaseModel):
    title: str
    publish: bool
    audio_ulid: str


class PlaylistUpdateIn(BaseModel):
    title: str
    description: str
    thumbnail_audio_ulid: str
    publish: bool
    audio_ulids: list[str]


class PlaylistAudioIn(BaseModel):
    audio_ulid: str


class PlaylistOut(BaseModel):
    ulid: str
    title: str
    image: str
    publish: bool
    count: int
    audio_ulids: list[str]
    updated: datetime


class PlaylistListOut(BaseModel):
    items: list[PlaylistOut]


class PlaylistDetailOut(BaseModel):
    ulid: str
    title: str
    description: str
    image: str
    thumbnail_audio_ulid: str
    publish: bool
    is_owner: bool
    updated: datetime
    author: AuthorOut
    audios: list[AudioOut]


class PlaylistCreateOut(BaseModel):
    ulid: str
