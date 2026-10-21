from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.subscribe.data import SubscribeData
from api.utils.common.result import FatalError, Result


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    user_id: int = 0
    channel_id: int = 0
    is_subscribe: bool | None = None


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class SubscribeInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[SubscribeData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[SubscribeData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        ...

    @abstractmethod
    def save_is_subscribe(self, id: int, is_subscribe: bool) -> Result[bool, FatalError]:
        ...
