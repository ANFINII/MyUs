from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.subscribe.data import SubscribeData


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    user_id: int = 0
    channel_id: int = 0
    is_subscribe: bool = False


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class SubscribeInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[SubscribeData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[SubscribeData]) -> None:
        ...

    @abstractmethod
    def count(self, filter: FilterOption) -> int:
        ...
