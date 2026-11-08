from dataclasses import replace
from datetime import datetime
from typing import assert_never
from api.src.domain.aggregate.subscription.event import SubscriptionActivated, SubscriptionCancellationScheduled, SubscriptionCancellationRequested, SubscriptionCancellationFailed, SubscriptionEnded, SubscriptionEvent, SubscriptionOpened, SubscriptionPaymentPastDue, SubscriptionPlanChanged, SubscriptionRenewed
from api.src.domain.aggregate.subscription.state import ActiveSubscription, EndedSubscription, IncompleteSubscription, PastDueSubscription, SubscriptionDetail, SubscriptionState
from api.src.domain.interface.es.data import EventEnvelope
from api.utils.common.result import HistoryCorruptedError, Result
from api.utils.enum.payment import SubscriptionStatus


def replay(history: list[EventEnvelope[SubscriptionEvent]]) -> Result[SubscriptionState | None, HistoryCorruptedError]:
    state: SubscriptionState | None = None
    for envelope in history:
        apply_ret = apply(state, envelope)
        if apply_ret.is_err:
            return Result.err(apply_ret.err_value)
        state = apply_ret.ok_value

    return Result.ok(state)


def apply(state: SubscriptionState | None, envelope: EventEnvelope[SubscriptionEvent]) -> Result[SubscriptionState, HistoryCorruptedError]:
    expected_seq = 1 if state is None else state.seq + 1
    if envelope.seq != expected_seq:
        return Result.err(HistoryCorruptedError(f"seq expected={expected_seq} actual={envelope.seq} aggregate_id={envelope.aggregate_id}"))

    seq = envelope.seq
    occurred_at = envelope.occurred_at
    match state, envelope.event:
        case None, SubscriptionOpened(detail=detail, status=status):
            return Result.ok(convert_state(detail, status, seq, occurred_at))
        case IncompleteSubscription(), SubscriptionActivated(current_period_end=current_period_end):
            return Result.ok(ActiveSubscription(detail=replace(state.detail, current_period_end=current_period_end), seq=seq, last_occurred_at=occurred_at, cancellation_request_id=""))
        case PastDueSubscription(), SubscriptionActivated(current_period_end=current_period_end):
            return Result.ok(ActiveSubscription(detail=replace(state.detail, current_period_end=current_period_end), seq=seq, last_occurred_at=occurred_at, cancellation_request_id=state.cancellation_request_id))
        case ActiveSubscription(), SubscriptionPaymentPastDue():
            return Result.ok(PastDueSubscription(detail=state.detail, seq=seq, last_occurred_at=occurred_at, cancellation_request_id=state.cancellation_request_id))
        case ActiveSubscription() | PastDueSubscription(), SubscriptionRenewed(current_period_end=current_period_end):
            return Result.ok(replace(state, detail=replace(state.detail, current_period_end=current_period_end), seq=seq, last_occurred_at=occurred_at))
        case IncompleteSubscription() | ActiveSubscription() | PastDueSubscription(), SubscriptionPlanChanged(product_code=product_code, price=price):
            return Result.ok(replace(state, detail=replace(state.detail, product_code=product_code, price=price), seq=seq, last_occurred_at=occurred_at))
        case IncompleteSubscription(), SubscriptionCancellationScheduled(canceled_at=canceled_at):
            return Result.ok(replace(state, detail=replace(state.detail, canceled_at=canceled_at), seq=seq, last_occurred_at=occurred_at))
        case ActiveSubscription() | PastDueSubscription(), SubscriptionCancellationScheduled(canceled_at=canceled_at):
            return Result.ok(replace(state, detail=replace(state.detail, canceled_at=canceled_at), seq=seq, last_occurred_at=occurred_at, cancellation_request_id=""))
        case ActiveSubscription() | PastDueSubscription(), SubscriptionCancellationRequested():
            return Result.ok(replace(state, seq=seq, cancellation_request_id=str(envelope.event_id)))
        case ActiveSubscription() | PastDueSubscription(), SubscriptionCancellationFailed():
            return Result.ok(replace(state, seq=seq, cancellation_request_id=""))
        case IncompleteSubscription() | ActiveSubscription() | PastDueSubscription(), SubscriptionEnded(status=status, canceled_at=canceled_at):
            return Result.ok(EndedSubscription(detail=replace(state.detail, canceled_at=canceled_at), status=status, seq=seq, last_occurred_at=occurred_at))
        case _:
            return Result.err(HistoryCorruptedError(f"event={type(envelope.event).__name__} not acceptable in state={type(state).__name__} aggregate_id={envelope.aggregate_id} seq={seq}"))


def convert_state(detail: SubscriptionDetail, status: SubscriptionStatus, seq: int, occurred_at: datetime) -> SubscriptionState:
    match status:
        case SubscriptionStatus.INCOMPLETE:
            return IncompleteSubscription(detail=detail, seq=seq, last_occurred_at=occurred_at)
        case SubscriptionStatus.ACTIVE:
            return ActiveSubscription(detail=detail, seq=seq, last_occurred_at=occurred_at, cancellation_request_id="")
        case SubscriptionStatus.PAST_DUE:
            return PastDueSubscription(detail=detail, seq=seq, last_occurred_at=occurred_at, cancellation_request_id="")
        case SubscriptionStatus.CANCELED | SubscriptionStatus.EXPIRED:
            return EndedSubscription(detail=detail, status=status, seq=seq, last_occurred_at=occurred_at)
        case _:
            assert_never(status)
