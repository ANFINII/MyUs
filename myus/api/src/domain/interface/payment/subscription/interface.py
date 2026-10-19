from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.payment.subscription.data import SubscriptionData
from api.utils.common.result import FatalError, Result


class SortType(Enum):
    STARTED_AT = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    customer_user_id: int = 0
    provider: str = ""
    external_id: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.STARTED_AT


class SubscriptionInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[SubscriptionData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[SubscriptionData]) -> Result[list[int], FatalError]:
        ...
