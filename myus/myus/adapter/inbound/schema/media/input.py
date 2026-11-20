from datetime import date, datetime
from pydantic import BaseModel
from myus.utils.enum.media import MediaType
from ..common import Title


class VideoIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: Title
    content: str


class AudioIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: Title
    content: str
    lyric: str


class BlogIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: Title
    content: str
    richtext: str
    paid_text: str
    price: int
    is_promotion: bool


class ComicIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: Title
    content: str


class PictureIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: Title
    content: str


class ChatIn(BaseModel):
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: Title
    content: str
    period: date


class VideoUpdateIn(BaseModel):
    category_ulid: str
    title: Title
    content: str
    publish: bool
    publish_at: datetime


class AudioUpdateIn(BaseModel):
    category_ulid: str
    title: Title
    content: str
    lyric: str
    publish: bool
    publish_at: datetime


class HiresIn(BaseModel):
    price: int


class BlogUpdateIn(BaseModel):
    category_ulid: str
    title: Title
    content: str
    richtext: str
    paid_text: str
    price: int
    is_promotion: bool
    publish: bool
    publish_at: datetime


class ComicUpdateIn(BaseModel):
    category_ulid: str
    title: Title
    content: str
    price: int
    publish: bool
    publish_at: datetime
    pages: list[str]
    free_pages: int


class PictureUpdateIn(BaseModel):
    category_ulid: str
    title: Title
    content: str
    publish: bool
    publish_at: datetime


class ChatUpdateIn(BaseModel):
    category_ulid: str
    title: Title
    content: str
    period: date
    publish: bool
    publish_at: datetime


class BulkDeleteIn(BaseModel):
    ulids: list[str]


class MediaReadIn(BaseModel):
    ulid: str
    media_type: MediaType
