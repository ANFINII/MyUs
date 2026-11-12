from dataclasses import dataclass, field
from enum import Enum, auto
from myus.utils.constants.page import PAGE_SIZE


class SortType(Enum):
    ID = auto()
    CREATED = auto()
    SCORE = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    ulids: list[str] = field(default_factory=list)
    publish: bool | None = None
    owner_id: int = 0
    channel_id: int = 0
    channel_ulid: str = ""
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


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = PAGE_SIZE
    offset: int = 0
