from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.media import CommentTypeNo
from .data import CommentData


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    id: int = 0
    ulid: str = ""
    type_no: CommentTypeNo | None = None
    object_id: int = 0
    user_id: int = 0
    is_parent: bool | None = None


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = 0
    offset: int = 0


class CommentInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[CommentData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[CommentData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def get_liked_ids(self, ids: list[int], user_id: int) -> Result[list[int], FatalError]:
        ...
