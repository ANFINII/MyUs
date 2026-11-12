from collections.abc import Callable
from datetime import datetime
from myus.domain.es.data import EventEnvelope
from myus.domain.es.interface import EventStoreInterface
from myus.utils.common.result import CommandError, ConflictError, FatalError, HistoryCorruptedError, Result, ValidateError
from myus.utils.functions.es import new_event_id


COMMAND_RETRY = 3


@Result.shield_exception()
def handle_command[S, E](
    repo: EventStoreInterface,
    aggregate_type: str,
    aggregate_id: str,
    replay: Callable[[list[EventEnvelope[E]]], Result[S, HistoryCorruptedError]],
    decide: Callable[[S], Result[list[E], ValidateError]],
    occurred_at: datetime,
) -> Result[list[EventEnvelope[E]], CommandError]:
    for _ in range(COMMAND_RETRY):
        load_ret = repo.load(aggregate_type, aggregate_id, 0)
        if load_ret.is_err:
            return Result.err(load_ret.err_value)

        history = load_ret.ok_value
        state_ret = replay(history)
        if state_ret.is_err:
            return Result.err(state_ret.err_value)

        state = state_ret.ok_value
        decide_ret = decide(state)
        if decide_ret.is_err:
            return Result.err(decide_ret.err_value)

        events = decide_ret.ok_value
        if len(events) == 0:
            return Result.ok([])

        last_seq = len(history)
        envelopes = [
            EventEnvelope(
                event_id=new_event_id(aggregate_type, aggregate_id, last_seq + i + 1),
                aggregate_type=aggregate_type,
                aggregate_id=aggregate_id,
                seq=last_seq + i + 1,
                occurred_at=occurred_at,
                event=event,
            )
            for i, event in enumerate(events)
        ]
        append_ret = repo.append(envelopes)
        if append_ret.is_ok:
            return Result.ok(envelopes)

        match append_ret.err_value:
            case ConflictError():
                continue
            case FatalError() as error:
                return Result.err(error)

    return Result.err(ConflictError(f"retry exhausted aggregate={aggregate_type}:{aggregate_id}"))
