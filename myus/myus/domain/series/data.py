from dataclasses import dataclass
from myus.utils.enum.media import MediaType


@dataclass(frozen=True, slots=True)
class SeriesData:
    id: int
    ulid: str
    channel_id: int
    media_type: MediaType
    title: str
    media_ids: list[int]
