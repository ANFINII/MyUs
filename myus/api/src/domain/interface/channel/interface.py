from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.channel.data import ChannelData


class SortType(Enum):
    CREATED = auto()
    UPDATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    owner_id: int = 0
    is_default: bool | None = None


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class ChannelInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[ChannelData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[ChannelData]) -> list[int]:
        ...

    @abstractmethod
    def delete(self, id: int) -> None:
        ...
