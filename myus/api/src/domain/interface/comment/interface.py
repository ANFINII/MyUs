from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from api.src.domain.interface.comment.data import CommentData
from api.utils.common.result import FatalError, Result
from api.utils.enum.media import CommentTypeNo


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    id: int = 0
    ulid: str = ""
    type_no: CommentTypeNo | None = None
    object_id: int = 0
    object_ids: list[int] = field(default_factory=list)
    user_id: int = 0
    is_parent: bool | None = None


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class CommentInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
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
