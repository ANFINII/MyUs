from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SubscribeOutData:
    is_subscribe: bool
    count: int
