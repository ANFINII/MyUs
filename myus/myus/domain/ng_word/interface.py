from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from myus.utils.common.result import FatalError, Result
from myus.utils.constants.page import PAGE_SIZE
from .data import NgWordData


class SortType(Enum):
    ID = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    search: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.ID


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = PAGE_SIZE
    offset: int = 0


class NgWordInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[NgWordData], FatalError]:
        ...
