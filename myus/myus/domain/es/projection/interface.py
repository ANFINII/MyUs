from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.es import ProjectorName
from .data import ProjectionProgressData


class SortType(Enum):
    ID = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    projector: ProjectorName | None = None
    aggregate_type: str = ""
    aggregate_id: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.ID


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = 0
    offset: int = 0


class ProjectionProgressInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[ProjectionProgressData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[ProjectionProgressData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...
