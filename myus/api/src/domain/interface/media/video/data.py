from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VideoData:
    id: int
    ulid: str
    channel_id: int
    title: str
    content: str
    image: str
    video: str
    convert: str
    read: int
    publish: bool
