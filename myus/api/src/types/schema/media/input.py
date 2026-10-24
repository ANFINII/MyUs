from pydantic import BaseModel
from api.utils.enum.media import MediaType


class VideoIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    title: str
    content: str


class MusicIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    title: str
    content: str
    lyric: str
    download: bool


class BlogIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    title: str
    content: str
    richtext: str
    is_promotion: bool


class ComicIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    title: str
    content: str


class PictureIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    title: str
    content: str


class ChatIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    title: str
    content: str
    period: str


class VideoUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    publish: bool


class MusicUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    lyric: str
    download: bool
    publish: bool


class BlogUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    richtext: str
    is_promotion: bool
    publish: bool


class ComicUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    publish: bool


class PictureUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    publish: bool


class ChatUpdateIn(BaseModel):
    category_ulid: str
    title: str
    content: str
    period: str
    publish: bool


class BulkDeleteIn(BaseModel):
    ulids: list[str]


class MediaReadIn(BaseModel):
    ulid: str
    media_type: MediaType
