from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from myus.utils.common.result import FatalError, Result
from .data import PlaylistData


class SortType(Enum):
    UPDATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    author_id: int = 0
    publish: bool | None = None


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.UPDATED


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = 0
    offset: int = 0


class PlaylistInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[PlaylistData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[PlaylistData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...
