from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class PlaylistData:
    id: int
    ulid: str
    author_id: int
    title: str
    description: str
    image: str
    publish: bool
    audio_ids: list[int]
    created: datetime
    updated: datetime
