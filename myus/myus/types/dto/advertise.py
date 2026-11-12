from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class AdvertiseCreateDTO:
    title: str
    url: str
    content: str
    publish: bool
    period: date


@dataclass(frozen=True, slots=True)
class AdvertiseUpdateDTO:
    title: str
    url: str
    content: str
    publish: bool
    period: date
