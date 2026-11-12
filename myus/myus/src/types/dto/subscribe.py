from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SubscribeDTO:
    is_subscribe: bool
    count: int
