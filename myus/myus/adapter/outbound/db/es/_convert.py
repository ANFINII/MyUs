from typing import Any
from pydantic import TypeAdapter
from myus.db.models.es import EsEvent, EsOutbox
from myus.domain.es.data import EventEnvelope


def convert_data(obj: EsEvent, event_class: type[Any]) -> EventEnvelope[Any]:
    return EventEnvelope(
        event_id=obj.event_id,
        aggregate_type=obj.aggregate_type,
        aggregate_id=obj.aggregate_id,
        seq=obj.seq,
        occurred_at=obj.occurred_at,
        event=TypeAdapter(event_class).validate_json(obj.payload),
    )


def marshal_data(data: EventEnvelope[Any], event_type: str) -> EsEvent:
    return EsEvent(
        event_id=data.event_id,
        aggregate_type=data.aggregate_type,
        aggregate_id=data.aggregate_id,
        seq=data.seq,
        event_type=event_type,
        payload=TypeAdapter(type(data.event)).dump_json(data.event).decode(),
        occurred_at=data.occurred_at,
    )


def marshal_outbox(data: EventEnvelope[Any]) -> EsOutbox:
    return EsOutbox(
        aggregate_type=data.aggregate_type,
        aggregate_id=data.aggregate_id,
        seq=data.seq,
    )
