from datetime import date, datetime
from pydantic import BaseModel
from myus.adapter.inbound.schema.common import Title, Url


class AdvertiseIn(BaseModel):
    title: Title
    url: Url
    content: str
    publish: bool
    period: date


class AdvertiseUpdateIn(BaseModel):
    title: Title
    url: Url
    content: str
    publish: bool
    period: date


class AdvertiseOut(BaseModel):
    ulid: str
    title: str
    url: str
    content: str
    image: str
    video: str
    read: int
    type: str
    period: date | None
    publish: bool
    created: datetime
    updated: datetime


class AdvertiseListOut(BaseModel):
    items: list[AdvertiseOut]
    total: int


class AdvertiseReadOut(BaseModel):
    read: int
