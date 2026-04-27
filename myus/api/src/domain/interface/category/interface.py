from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from api.src.domain.interface.category.data import CategoryData
from api.utils.enum.index import MediaType


class SortType(Enum):
    ID = auto()
    JP_NAME = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulids: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.ID


class CategoryInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[CategoryData]:
        ...

    @abstractmethod
    def bulk_save(self, media_type: MediaType, media_id: int, objs: list[CategoryData]) -> list[int]:
        ...
