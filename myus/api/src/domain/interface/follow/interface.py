from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.follow.data import FollowData
from api.utils.common.result import FatalError, Result


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    follower_id: int = 0
    following_id: int = 0
    is_follow: bool | None = None
    search: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class FollowInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[FollowData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[FollowData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        ...

    @abstractmethod
    def save_is_follow(self, id: int, is_follow: bool) -> Result[bool, FatalError]:
        ...
