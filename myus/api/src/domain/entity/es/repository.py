from typing import Any
import pydantic
from django.db import IntegrityError, transaction
from api.db.models.es import EsEvent, EsOutbox
from api.src.domain.entity.es._convert import convert_data, marshal_data, marshal_outbox
from api.src.domain.interface.es.data import EventEnvelope
from api.src.domain.interface.es.interface import EventStoreInterface
from api.utils.common.result import AppendError, ConflictError, FatalError, HistoryCorruptedError, HistoryError, Result


class EventStoreRepository(EventStoreInterface):
    def __init__(self, event_classes: dict[str, type[Any]]) -> None:
        self.event_classes = event_classes
        self.event_types = {event_class: event_type for event_type, event_class in event_classes.items()}

    @Result.shield_exception()
    def load(self, aggregate_type: str, aggregate_id: str, after_seq: int) -> Result[list[EventEnvelope[Any]], HistoryError]:
        objs = list(EsEvent.objects.filter(aggregate_type=aggregate_type, aggregate_id=aggregate_id, seq__gt=after_seq).order_by("seq"))
        envelopes: list[EventEnvelope[Any]] = []
        for i, obj in enumerate(objs):
            if obj.seq != after_seq + i + 1:
                return Result.err(HistoryCorruptedError(f"seq gap aggregate={aggregate_type}:{aggregate_id} expected={after_seq + i + 1} actual={obj.seq}"))

            event_class = self.event_classes.get(obj.event_type)
            if event_class is None:
                return Result.err(HistoryCorruptedError(f"unknown event_type={obj.event_type} aggregate={aggregate_type}:{aggregate_id} seq={obj.seq}"))

            try:
                envelopes.append(convert_data(obj, event_class))
            except pydantic.ValidationError as e:
                return Result.err(HistoryCorruptedError(f"invalid payload aggregate={aggregate_type}:{aggregate_id} seq={obj.seq} error={e}"))

        return Result.ok(envelopes)

    @Result.shield_exception()
    def append(self, envelopes: list[EventEnvelope[Any]]) -> Result[None, AppendError]:
        if len(envelopes) == 0:
            return Result.ok(None)

        models: list[EsEvent] = []
        for envelope in envelopes:
            event_type = self.event_types.get(type(envelope.event))
            if event_type is None:
                return Result.err(FatalError(f"unregistered event={type(envelope.event).__name__}"))
            models.append(marshal_data(envelope, event_type))

        try:
            with transaction.atomic():
                EsEvent.objects.bulk_create(models)
                EsOutbox.objects.bulk_create([marshal_outbox(envelope) for envelope in envelopes])
        except IntegrityError as e:
            return Result.err(ConflictError(f"aggregate={envelopes[0].aggregate_type}:{envelopes[0].aggregate_id} seq={envelopes[0].seq} error={e}"))

        return Result.ok(None)
