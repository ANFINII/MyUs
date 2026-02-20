from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.message.data import MessageData


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    chat_id: int = 0
    is_parent: bool = True


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class MessageInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[MessageData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[MessageData]) -> None:
        ...
