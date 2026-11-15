from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from myus.utils.common.result import FatalError, Result
from .data import LedgerEntryData


class SortType(Enum):
    OCCURRED_AT = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    transaction_id: int = 0
    external_ids: list[str] = field(default_factory=list)
    occurred_from: datetime | None = None
    occurred_to: datetime | None = None


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.OCCURRED_AT


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = 20
    offset: int = 0


class LedgerEntryInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[LedgerEntryData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[LedgerEntryData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...
