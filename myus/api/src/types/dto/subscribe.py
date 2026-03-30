from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SubscribeOutDTO:
    is_subscribe: bool
    count: int
