from dataclasses import dataclass
from datetime import date, datetime
from api.src.domain.interface.channel.data import ChannelData


@dataclass(frozen=True, slots=True)
class ChatData:
    id: int
    ulid: str
    title: str
    content: str
    read: int
    like: int
    period: date
    publish: bool
    created: datetime
    updated: datetime
    thread_count: int
    joined_count: int
    channel: ChannelData
