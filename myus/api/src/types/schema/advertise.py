from datetime import date, datetime
from pydantic import BaseModel


class AdvertiseIn(BaseModel):
    title: str
    url: str
    content: str
    publish: bool
    period: date | None = None


class AdvertiseUpdateIn(BaseModel):
    title: str
    url: str
    content: str
    publish: bool
    period: date | None = None


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
    datas: list[AdvertiseOut]
    total: int


class AdvertiseReadOut(BaseModel):
    read: int
