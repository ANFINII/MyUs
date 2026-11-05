from dataclasses import dataclass
from datetime import datetime, timezone
import pytest
from api.db.models.es import EsEvent, EsOutbox
from api.src.domain.entity.es.repository import EventStoreRepository
from api.src.domain.interface.es.data import EventEnvelope
from api.src.usecase.command.handler import handle_command
from api.utils.common.result import ConflictError, HistoryCorruptedError, Result, ValidateError
from api.utils.functions.es import new_event_id


pytestmark = pytest.mark.django_db

AGGREGATE_TYPE = "Counter"
AGGREGATE_ID = "01COUNTER"
NOW = datetime(2026, 11, 5, tzinfo=timezone.utc)


@dataclass(frozen=True, slots=True)
class CounterIncremented:
    amount: int


def store() -> EventStoreRepository:
    return EventStoreRepository({"Counter.Incremented.V1": CounterIncremented})


def envelope(seq: int, amount: int = 1) -> EventEnvelope[CounterIncremented]:
    return EventEnvelope(
        event_id=new_event_id(AGGREGATE_TYPE, AGGREGATE_ID, seq),
        aggregate_type=AGGREGATE_TYPE,
        aggregate_id=AGGREGATE_ID,
        seq=seq,
        occurred_at=NOW,
        event=CounterIncremented(amount=amount),
    )


def replay(history: list[EventEnvelope[CounterIncremented]]) -> Result[int, HistoryCorruptedError]:
    return Result.ok(sum(e.event.amount for e in history))


def increment(state: int) -> Result[list[CounterIncremented], ValidateError]:
    return Result.ok([CounterIncremented(amount=1)])


def test_appended_events_are_loaded_in_order() -> None:
    assert store().append([envelope(1, 5), envelope(2, 7)]).is_ok

    ret = store().load(AGGREGATE_TYPE, AGGREGATE_ID, 0)

    assert ret.is_ok, ret
    assert [(e.seq, e.event) for e in ret.ok_value] == [(1, CounterIncremented(5)), (2, CounterIncremented(7))]
    assert EsOutbox.objects.count() == 2


def test_same_seq_is_conflict() -> None:
    assert store().append([envelope(1)]).is_ok

    ret = store().append([envelope(1)])

    assert ret.is_err
    assert isinstance(ret.err_value, ConflictError)
    assert EsEvent.objects.count() == 1
    assert EsOutbox.objects.count() == 1


def test_conflict_rolls_back_event_and_outbox() -> None:
    assert store().append([envelope(1)]).is_ok

    ret = store().append([envelope(2), envelope(1)])

    assert ret.is_err
    assert list(EsEvent.objects.values_list("seq", flat=True)) == [1]
    assert list(EsOutbox.objects.values_list("seq", flat=True)) == [1]


def test_seq_gap_is_history_corrupted() -> None:
    assert store().append([envelope(1)]).is_ok
    EsEvent.objects.filter(seq=1).update(seq=2)

    ret = store().load(AGGREGATE_TYPE, AGGREGATE_ID, 0)

    assert ret.is_err
    assert isinstance(ret.err_value, HistoryCorruptedError)


def test_unknown_event_type_is_history_corrupted() -> None:
    assert store().append([envelope(1)]).is_ok

    ret = EventStoreRepository({}).load(AGGREGATE_TYPE, AGGREGATE_ID, 0)

    assert ret.is_err
    assert isinstance(ret.err_value, HistoryCorruptedError)


def test_command_is_retried_after_conflict() -> None:
    repo = store()
    calls: list[int] = []

    def increment_with_concurrent_write(state: int) -> Result[list[CounterIncremented], ValidateError]:
        if len(calls) == 0:
            assert repo.append([envelope(1, 10)]).is_ok
        calls.append(state)
        return Result.ok([CounterIncremented(amount=1)])

    ret = handle_command(repo, AGGREGATE_TYPE, AGGREGATE_ID, replay, increment_with_concurrent_write, NOW)

    assert ret.is_ok, ret
    assert calls == [0, 10]
    assert [e.seq for e in ret.ok_value] == [2]
    assert replay(repo.load(AGGREGATE_TYPE, AGGREGATE_ID, 0).ok_value).ok_value == 11


def test_command_without_events_saves_nothing() -> None:
    ret = handle_command(store(), AGGREGATE_TYPE, AGGREGATE_ID, replay, lambda state: Result.ok([]), NOW)

    assert ret.is_ok, ret
    assert EsEvent.objects.count() == 0


def test_command_appends_next_seq() -> None:
    repo = store()
    assert handle_command(repo, AGGREGATE_TYPE, AGGREGATE_ID, replay, increment, NOW).is_ok

    ret = handle_command(repo, AGGREGATE_TYPE, AGGREGATE_ID, replay, increment, NOW)

    assert ret.is_ok, ret
    assert [e.seq for e in ret.ok_value] == [2]
    assert ret.ok_value[0].event_id == new_event_id(AGGREGATE_TYPE, AGGREGATE_ID, 2)
