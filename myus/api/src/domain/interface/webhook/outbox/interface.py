from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.webhook.outbox.data import WebhookOutboxData
from api.utils.common.result import FatalError, Result


class SortType(Enum):
    OCCURRED_AT = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    provider: str = ""
    external_id: str = ""
    status: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.OCCURRED_AT


class WebhookOutboxInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[WebhookOutboxData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[WebhookOutboxData]) -> Result[list[int], FatalError]:
        ...
