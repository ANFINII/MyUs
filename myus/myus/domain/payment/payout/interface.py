from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from myus.domain.payment.payout.data import PayoutData
from myus.utils.common.result import FatalError, Result


class SortType(Enum):
    ARRIVAL_AT = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    provider: str = ""
    external_id: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.ARRIVAL_AT


class PayoutInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[PayoutData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[PayoutData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...
