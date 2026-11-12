from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HashtagDTO:
    ulid: str
    name: str
