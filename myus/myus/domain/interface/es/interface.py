from abc import ABC, abstractmethod
from typing import Any
from myus.domain.interface.es.data import EventEnvelope
from myus.utils.common.result import AppendError, HistoryError, Result


class EventStoreInterface(ABC):
    @abstractmethod
    def load(self, aggregate_type: str, aggregate_id: str, after_seq: int) -> Result[list[EventEnvelope[Any]], HistoryError]:
        ...

    @abstractmethod
    def append(self, envelopes: list[EventEnvelope[Any]]) -> Result[None, AppendError]:
        ...
