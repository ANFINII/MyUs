from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.comment.data import CommentData
from api.utils.enum.index import CommentTypeNo


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    id: int = 0
    ulid: str = ""
    type_no: CommentTypeNo | None = None
    object_id: int = 0
    user_id: int = 0
    is_parent: bool = False


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class CommentInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[CommentData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[CommentData]) -> None:
        ...

    @abstractmethod
    def get_liked_ids(self, ids: list[int], user_id: int) -> list[int]:
        ...
