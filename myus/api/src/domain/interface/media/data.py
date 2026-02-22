from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MediaCreateData:
    ulid: str


@dataclass(frozen=True, slots=True)
class HashtagData:
    jp_name: str
