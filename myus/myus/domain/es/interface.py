from abc import ABC, abstractmethod
from typing import Any
from myus.utils.common.result import AppendError, HistoryError, Result
from .data import EventEnvelope


class EventStoreInterface(ABC):
    @abstractmethod
    def load(self, aggregate_type: str, aggregate_id: str, after_seq: int) -> Result[list[EventEnvelope[Any]], HistoryError]:
        ...

    @abstractmethod
    def append(self, envelopes: list[EventEnvelope[Any]]) -> Result[None, AppendError]:
        ...
