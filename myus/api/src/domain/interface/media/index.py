from dataclasses import dataclass
from enum import Enum, auto


RECOMMEND_DAYS = 200
RECOMMEND_MIN_SCORE = 10.0


class SortType(Enum):
    ID = auto()
    CREATED = auto()
    SCORE = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    publish: bool | None = None
    owner_id: int = 0
    channel_id: int = 0
    category_id: int = 0
    is_recommend: bool = False
    search: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.ID


@dataclass(frozen=True, slots=True)
class ExcludeOption:
    id: int = 0
