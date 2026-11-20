from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from myus.utils.common.result import FatalError, Result
from .data import AudioHiresData


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    audio_id: int = 0


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.CREATED


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = 0
    offset: int = 0


class AudioHiresInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[AudioHiresData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[AudioHiresData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...
