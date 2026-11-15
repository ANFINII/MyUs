from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from myus.utils.common.result import FatalError, Result
from .data import SearchTagData
from .validation import SEARCH_TAG_MAX_COUNT


class SortType(Enum):
    SEQUENCE = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    author_id: int = 0


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.SEQUENCE


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = SEARCH_TAG_MAX_COUNT
    offset: int = 0


class SearchTagInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[SearchTagData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[SearchTagData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...
