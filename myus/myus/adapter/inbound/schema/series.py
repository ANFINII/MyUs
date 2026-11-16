from pydantic import BaseModel
from myus.utils.enum.media import MediaType
from .common import Title


class SeriesIn(BaseModel):
    channel_ulid: str
    media_type: MediaType
    title: Title


class SeriesUpdateIn(BaseModel):
    title: Title
    media_ulids: list[str]


class SeriesOut(BaseModel):
    ulid: str
    title: str
    media_type: MediaType
    count: int


class SeriesListOut(BaseModel):
    items: list[SeriesOut]


class ChannelSeriesOut(BaseModel):
    ulid: str
    title: str
    media_type: MediaType
    count: int
    media_ulid: str
    image: str


class ChannelSeriesListOut(BaseModel):
    items: list[ChannelSeriesOut]


class SeriesItemOut(BaseModel):
    ulid: str
    title: str
    publish: bool


class SeriesDetailOut(BaseModel):
    ulid: str
    title: str
    media_type: MediaType
    channel_ulid: str
    items: list[SeriesItemOut]
    candidates: list[SeriesItemOut]


class SeriesCreateOut(BaseModel):
    ulid: str
