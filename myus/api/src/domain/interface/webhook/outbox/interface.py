from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.webhook.outbox.data import WebhookOutboxData


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
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[WebhookOutboxData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[WebhookOutboxData]) -> list[int]:
        ...
