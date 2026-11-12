from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from myus.domain.payment.event.data import PaymentEventData
from myus.utils.common.result import FatalError, Result


class SortType(Enum):
    OCCURRED_AT = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    provider: str = ""
    event_id: str = ""
    is_processed: bool | None = None
    max_attempts: int = 0


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.OCCURRED_AT


class PaymentEventInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[PaymentEventData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[PaymentEventData]) -> Result[list[int], FatalError]:
        ...
