from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SubscribeData:
    id: int
    user_id: int
    channel_id: int
    is_subscribe: bool
