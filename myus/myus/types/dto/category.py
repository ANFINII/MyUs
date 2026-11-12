from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CategoryDTO:
    ulid: str
    jp_name: str
    en_name: str
