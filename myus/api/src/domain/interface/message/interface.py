from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from api.src.domain.interface.message.data import MessageData
from api.utils.common.result import FatalError, Result


class SortType(Enum):
    CREATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    chat_id: int = 0
    chat_ids: list[int] = field(default_factory=list)
    message_ulid: str = ""
    parent_ulid: str = ""
    is_parent: bool | None = True


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class MessageInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[MessageData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[MessageData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...
