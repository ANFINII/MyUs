from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.es.subscription_lookup.data import SubscriptionLookupData
from api.utils.common.result import FatalError, Result


class SortType(Enum):
    ID = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    provider: str = ""
    external_id: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.ID


class SubscriptionLookupInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[SubscriptionLookupData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[SubscriptionLookupData]) -> Result[list[int], FatalError]:
        ...
