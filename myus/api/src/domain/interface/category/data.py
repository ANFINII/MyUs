from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CategoryData:
    id: int
    ulid: str
    jp_name: str
    en_name: str
