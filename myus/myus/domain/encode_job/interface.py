from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from myus.utils.common.result import FatalError, Result
from .data import EncodeJobData


class SortType(Enum):
    ID = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    is_processed: bool | None = None
    max_attempts: int = 0


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.ID


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = 0
    offset: int = 0


class EncodeJobInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[EncodeJobData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[EncodeJobData]) -> Result[list[int], FatalError]:
        ...
