from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class AdvertiseData:
    id: int
    ulid: str
    author_id: int
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
