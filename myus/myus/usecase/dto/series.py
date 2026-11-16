from dataclasses import dataclass
from myus.utils.enum.media import MediaType


@dataclass(frozen=True, slots=True)
class SeriesDTO:
    ulid: str
    title: str
    media_type: MediaType
    count: int


@dataclass(frozen=True, slots=True)
class SeriesItemDTO:
    ulid: str
    title: str
    publish: bool


@dataclass(frozen=True, slots=True)
class SeriesDetailDTO:
    ulid: str
    title: str
    media_type: MediaType
    channel_ulid: str
    items: list[SeriesItemDTO]
    candidates: list[SeriesItemDTO]


@dataclass(frozen=True, slots=True)
class ChannelSeriesDTO:
    ulid: str
    title: str
    media_type: MediaType
    count: int
    media_ulid: str
    image: str


@dataclass(frozen=True, slots=True)
class SeriesCreateDTO:
    channel_ulid: str
    media_type: MediaType
    title: str


@dataclass(frozen=True, slots=True)
class SeriesUpdateDTO:
    title: str
    media_ulids: list[str]


@dataclass(frozen=True, slots=True)
class MediaSeriesDTO:
    ulid: str
    title: str
    media_ids: list[int]
