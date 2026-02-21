from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.user.data import UserAllData
from api.utils.enum.index import MediaType


class SortType(Enum):
    CREATED = auto()
    NICKNAME = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    id: int = 0
    ulid: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class UserInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[UserAllData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[UserAllData]) -> list[int]:
        ...

    @abstractmethod
    def media_like(self, user_id: int, media_type: MediaType, media_id: int) -> tuple[bool, int]:
        ...

    @abstractmethod
    def comment_like(self, user_id: int, comment_id: int) -> tuple[bool, int]:
        ...
