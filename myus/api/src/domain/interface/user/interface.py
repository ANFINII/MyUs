from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.user.data import UserAllData
from api.utils.common.result import FatalError, Result
from api.utils.enum.media import MediaType


class SortType(Enum):
    CREATED = auto()
    NICKNAME = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    id: int = 0
    ulid: str = ""
    email: str = ""
    username: str = ""
    nickname: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class UserInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption | None = None) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[UserAllData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[UserAllData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def authenticate(self, login_id: str, password: str) -> Result[int | None, FatalError]:
        ...

    @abstractmethod
    def media_like(self, user_id: int, media_type: MediaType, media_id: int) -> Result[tuple[bool, int], FatalError]:
        ...

    @abstractmethod
    def comment_like(self, user_id: int, comment_id: int) -> Result[tuple[bool, int], FatalError]:
        ...

    @abstractmethod
    def save_follow_count(self, follower_id: int, following_id: int, follower_count: int, following_count: int) -> Result[None, FatalError]:
        ...
