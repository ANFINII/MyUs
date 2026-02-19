from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChannelData:
    id: int
    ulid: str
    owner_id: int
    avatar: str
    name: str
    description: str
    is_default: bool
    count: int
