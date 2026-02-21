from dataclasses import dataclass
from enum import Enum, auto


class SortType(Enum):
    ID = auto()
    CREATED = auto()
    SCORE = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    publish: bool | None = None
    category_id: int = 0
    search: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.ID


@dataclass(frozen=True, slots=True)
class ExcludeOption:
    id: int | None = None
