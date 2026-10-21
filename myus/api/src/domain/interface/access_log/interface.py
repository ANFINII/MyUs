from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.access_log.data import AccessLogData
from api.utils.common.result import FatalError, Result
from api.utils.enum.access_log import AccessType


class SortType(Enum):
    UPDATED = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ip_address: str = ""
    type: AccessType | None = None
    type_id: int = 0


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.UPDATED


class AccessLogInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[AccessLogData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[AccessLogData]) -> Result[list[int], FatalError]:
        ...
