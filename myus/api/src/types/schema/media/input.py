from datetime import datetime
from pydantic import BaseModel
from api.utils.enum.media import MediaType


class VideoIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str


class MusicIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str
    lyric: str
    download: bool


class BlogIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str
    richtext: str
    is_promotion: bool


class ComicIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str


class PictureIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str


class ChatIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str
    period: str


class VideoUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    publish: bool
    publish_at: datetime


class MusicUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    lyric: str
    download: bool
    publish: bool
    publish_at: datetime


class BlogUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    richtext: str
    is_promotion: bool
    publish: bool
    publish_at: datetime


class ComicUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    publish: bool
    publish_at: datetime


class PictureUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    publish: bool
    publish_at: datetime


class ChatUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    period: str
    publish: bool
    publish_at: datetime


class BulkDeleteIn(BaseModel):
    ulids: list[str]


class MediaReadIn(BaseModel):
    ulid: str
    media_type: MediaType
