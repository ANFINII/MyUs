from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.access_log.data import AccessLogData
from api.utils.enum.media import MediaType


class SortType(Enum):
    UPDATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ip_address: str = ""
    type: MediaType | None = None
    type_id: int = 0


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.UPDATED


class AccessLogInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[AccessLogData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[AccessLogData]) -> list[int]:
        ...
