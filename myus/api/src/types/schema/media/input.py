from pydantic import BaseModel


class VideoIn(BaseModel):
    channel_ulid: str
    publish: bool
    title: str
    content: str


class MusicIn(BaseModel):
    channel_ulid: str
    publish: bool
    title: str
    content: str
    lyric: str
    download: bool


class ComicIn(BaseModel):
    channel_ulid: str
    publish: bool
    title: str
    content: str


class PictureIn(BaseModel):
    channel_ulid: str
    publish: bool
    title: str
    content: str


class BlogIn(BaseModel):
    channel_ulid: str
    publish: bool
    title: str
    content: str
    richtext: str


class ChatIn(BaseModel):
    channel_ulid: str
    publish: bool
    title: str
    content: str
    period: str


class VideoUpdateIn(BaseModel):
    title: str
    content: str
    publish: bool


class MusicUpdateIn(BaseModel):
    title: str
    content: str
    lyric: str
    download: bool
    publish: bool


class ComicUpdateIn(BaseModel):
    title: str
    content: str
    publish: bool


class BulkDeleteIn(BaseModel):
    ulids: list[str]
