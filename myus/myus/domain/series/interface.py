from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.media import MediaType
from .data import SeriesData


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    channel_id: int = 0
    media_type: MediaType | None = None
    media_ids: list[int] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = 0
    offset: int = 0


class SeriesInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[SeriesData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[SeriesData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...
