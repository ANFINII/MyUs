from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from api.src.domain.interface.payment.webhook_event.data import WebhookEventData


class SortType(Enum):
    OCCURRED_AT = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    provider: str = ""
    event_id: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.OCCURRED_AT


class WebhookEventInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[WebhookEventData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[WebhookEventData]) -> list[int]:
        ...
