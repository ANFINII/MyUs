from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from api.src.domain.interface.notification.data import NotificationData
from api.utils.common.result import FatalError, Result
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    type_no: NotificationTypeNo | None = None
    object_type: NotificationObjectType | None = None
    object_ids: list[int] = field(default_factory=list)
    user_to_id: int = 0
    receiver_id: int = 0
    enabled_types: tuple[NotificationTypeNo, ...] = ()
    confirmed_user_id: int = 0
    exclude_user_id: int = 0


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class NotificationInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[NotificationData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[NotificationData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...

    @abstractmethod
    def delete(self, type_no: NotificationTypeNo, object_type: NotificationObjectType, object_id: int, user_from_id: int) -> Result[None, FatalError]:
        ...

    @abstractmethod
    def delete_by_user(self, ulid: str, user_id: int) -> Result[None, FatalError]:
        ...

    @abstractmethod
    def confirm(self, ulid: str, user_id: int) -> Result[None, FatalError]:
        ...
