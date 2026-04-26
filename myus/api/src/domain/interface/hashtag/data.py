from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HashtagData:
    id: int
    ulid: str
    name: str
