from datetime import datetime
from pydantic import BaseModel
from .media.output import MusicOut


class PlaylistIn(BaseModel):
    title: str
    publish: bool
    music_ulid: str


class PlaylistUpdateIn(BaseModel):
    title: str
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
    updated: datetime


class PlaylistListOut(BaseModel):
    items: list[PlaylistOut]


class PlaylistDetailOut(BaseModel):
    ulid: str
    title: str
    publish: bool
    is_owner: bool
    author_ulid: str
    author_nickname: str
    musics: list[MusicOut]
    updated: datetime


class PlaylistCreateOut(BaseModel):
    ulid: str
