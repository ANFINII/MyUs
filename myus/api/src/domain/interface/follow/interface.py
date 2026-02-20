from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.follow.data import FollowData


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    follower_id: int = 0
    following_id: int = 0
    search: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class FollowInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[FollowData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[FollowData]) -> None:
        ...

    @abstractmethod
    def count(self, filter: FilterOption) -> int:
        ...
