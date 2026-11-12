from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class AdvertiseInDTO:
    title: str
    url: str
    content: str
    publish: bool
    period: date
