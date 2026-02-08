from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PictureData:
    id: int
    ulid: str
    channel_id: int
    title: str
    content: str
    image: str
    read: int
    publish: bool
