from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.notification.data import NotificationData
from api.utils.enum.index import NotificationTypeNo


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    type_no: NotificationTypeNo | None = None
    object_id: int = 0
    user_to_id: int = 0


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class NotificationInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[NotificationData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[NotificationData]) -> None:
        ...

    @abstractmethod
    def delete(self, type_no: NotificationTypeNo, object_id: int) -> None:
        ...
