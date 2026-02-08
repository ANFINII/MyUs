from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SearchTagData:
    id: int
    author_id: int
    sequence: int
    name: str
