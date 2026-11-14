from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from myus.utils.common.result import FatalError, Result
from myus.utils.constants.page import PAGE_SIZE
from .data import AdvertiseData


class SortType(Enum):
    ID = auto()
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    ulids: list[str] = field(default_factory=list)
    publish: bool | None = None
    owner_id: int = 0
    search: str = ""
    advertise_type: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.ID


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = PAGE_SIZE
    offset: int = 0


class AdvertiseInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[AdvertiseData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[AdvertiseData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...

    @abstractmethod
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        ...

    @abstractmethod
    def save_read(self, media_id: int) -> Result[int, FatalError]:
        ...
