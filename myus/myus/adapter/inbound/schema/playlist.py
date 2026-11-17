from datetime import datetime
from pydantic import BaseModel
from .media.output import MusicOut
from .user import AuthorOut


class PlaylistIn(BaseModel):
    title: str
    publish: bool
    music_ulid: str


class PlaylistUpdateIn(BaseModel):
    title: str
    description: str
    thumbnail_music_ulid: str
    publish: bool
    music_ulids: list[str]


class PlaylistMusicIn(BaseModel):
    music_ulid: str


class PlaylistOut(BaseModel):
    ulid: str
    title: str
    publish: bool
    count: int
    image: str
    music_ulids: list[str]
    updated: datetime


class PlaylistListOut(BaseModel):
    items: list[PlaylistOut]


class PlaylistDetailOut(BaseModel):
    ulid: str
    title: str
    description: str
    image: str
    thumbnail_music_ulid: str
    publish: bool
    is_owner: bool
    updated: datetime
    author: AuthorOut
    musics: list[MusicOut]


class PlaylistCreateOut(BaseModel):
    ulid: str
