from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.channel.data import ChannelData
from api.utils.common.result import FatalError, Result


class SortType(Enum):
    ID = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    owner_id: int = 0
    is_default: bool | None = None


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.ID


class ChannelInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[ChannelData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[ChannelData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def delete(self, id: int) -> Result[None, FatalError]:
        ...

    @abstractmethod
    def save_count(self, id: int, count: int) -> Result[None, FatalError]:
        ...
