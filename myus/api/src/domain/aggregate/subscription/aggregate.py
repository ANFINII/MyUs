from dataclasses import replace
from datetime import datetime
from typing import assert_never
from api.src.domain.aggregate.subscription.data import ActiveSubscription, EndedSubscription, IncompleteSubscription, PastDueSubscription, SubscriptionActivated, SubscriptionCancellationScheduled, SubscriptionDetail, SubscriptionEnded, SubscriptionEvent, SubscriptionOpened, SubscriptionPaymentPastDue, SubscriptionPlanChanged, SubscriptionRenewed, SubscriptionState
from api.src.domain.interface.es.data import EventEnvelope
from api.src.domain.interface.payment.event.data import ProviderSubscriptionData
from api.utils.common.result import HistoryCorruptedError, Result, ValidateError
from api.utils.enum.payment import SubscriptionStatus


def accept_provider_state(state: SubscriptionState | None, provider: ProviderSubscriptionData, occurred_at: datetime) -> Result[list[SubscriptionEvent], ValidateError]:
    detail = subscription_detail(provider)
    if state is None:
        return Result.ok([SubscriptionOpened(detail=detail, status=provider.status)])

    if isinstance(state, EndedSubscription) or occurred_at < state.last_occurred_at:
        return Result.ok([])

    events: list[SubscriptionEvent] = []
    if detail.product_code != state.detail.product_code or detail.price != state.detail.price:
        events.append(SubscriptionPlanChanged(product_code=detail.product_code, price=detail.price))

    is_period_changed = detail.current_period_end != state.detail.current_period_end
    match provider.status:
        case SubscriptionStatus.INCOMPLETE:
            return Result.ok([])
        case SubscriptionStatus.ACTIVE:
            match state:
                case IncompleteSubscription() | PastDueSubscription():
                    events.append(SubscriptionActivated(current_period_end=detail.current_period_end))
                case ActiveSubscription():
                    if is_period_changed:
                        events.append(SubscriptionRenewed(current_period_end=detail.current_period_end))
        case SubscriptionStatus.PAST_DUE:
            match state:
                case IncompleteSubscription():
                    events.extend([SubscriptionActivated(current_period_end=detail.current_period_end), SubscriptionPaymentPastDue()])
                case ActiveSubscription():
                    if is_period_changed:
                        events.append(SubscriptionRenewed(current_period_end=detail.current_period_end))
                    events.append(SubscriptionPaymentPastDue())
                case PastDueSubscription():
                    if is_period_changed:
                        events.append(SubscriptionRenewed(current_period_end=detail.current_period_end))
        case SubscriptionStatus.CANCELED | SubscriptionStatus.EXPIRED:
            events.append(SubscriptionEnded(status=provider.status, canceled_at=detail.canceled_at))
            return Result.ok(events)
        case _:
            assert_never(provider.status)

    if detail.canceled_at != state.detail.canceled_at:
        events.append(SubscriptionCancellationScheduled(canceled_at=detail.canceled_at))
    return Result.ok(events)


def replay_subscription(history: list[EventEnvelope[SubscriptionEvent]]) -> Result[SubscriptionState | None, HistoryCorruptedError]:
    state: SubscriptionState | None = None
    for envelope in history:
        apply_ret = apply_subscription(state, envelope)
        if apply_ret.is_err:
            return Result.err(apply_ret.err_value)
        state = apply_ret.ok_value

    return Result.ok(state)


def apply_subscription(state: SubscriptionState | None, envelope: EventEnvelope[SubscriptionEvent]) -> Result[SubscriptionState, HistoryCorruptedError]:
    expected_seq = 1 if state is None else state.seq + 1
    if envelope.seq != expected_seq:
        return Result.err(HistoryCorruptedError(f"seq expected={expected_seq} actual={envelope.seq} aggregate_id={envelope.aggregate_id}"))

    seq = envelope.seq
    occurred_at = envelope.occurred_at
    match state, envelope.event:
        case None, SubscriptionOpened(detail=detail, status=status):
            return Result.ok(subscription_state(detail, status, seq, occurred_at))
        case IncompleteSubscription() | PastDueSubscription(), SubscriptionActivated(current_period_end=current_period_end):
            return Result.ok(ActiveSubscription(detail=replace(state.detail, current_period_end=current_period_end), seq=seq, last_occurred_at=occurred_at))
        case ActiveSubscription(), SubscriptionPaymentPastDue():
            return Result.ok(PastDueSubscription(detail=state.detail, seq=seq, last_occurred_at=occurred_at))
        case ActiveSubscription() | PastDueSubscription(), SubscriptionRenewed(current_period_end=current_period_end):
            return Result.ok(replace(state, detail=replace(state.detail, current_period_end=current_period_end), seq=seq, last_occurred_at=occurred_at))
        case IncompleteSubscription() | ActiveSubscription() | PastDueSubscription(), SubscriptionPlanChanged(product_code=product_code, price=price):
            return Result.ok(replace(state, detail=replace(state.detail, product_code=product_code, price=price), seq=seq, last_occurred_at=occurred_at))
        case IncompleteSubscription() | ActiveSubscription() | PastDueSubscription(), SubscriptionCancellationScheduled(canceled_at=canceled_at):
            return Result.ok(replace(state, detail=replace(state.detail, canceled_at=canceled_at), seq=seq, last_occurred_at=occurred_at))
        case IncompleteSubscription() | ActiveSubscription() | PastDueSubscription(), SubscriptionEnded(status=status, canceled_at=canceled_at):
            return Result.ok(EndedSubscription(detail=replace(state.detail, canceled_at=canceled_at), status=status, seq=seq, last_occurred_at=occurred_at))
        case _:
            return Result.err(HistoryCorruptedError(f"event={type(envelope.event).__name__} not acceptable in state={type(state).__name__} aggregate_id={envelope.aggregate_id} seq={seq}"))


def subscription_state(detail: SubscriptionDetail, status: SubscriptionStatus, seq: int, occurred_at: datetime) -> SubscriptionState:
    match status:
        case SubscriptionStatus.INCOMPLETE:
            return IncompleteSubscription(detail=detail, seq=seq, last_occurred_at=occurred_at)
        case SubscriptionStatus.ACTIVE:
            return ActiveSubscription(detail=detail, seq=seq, last_occurred_at=occurred_at)
        case SubscriptionStatus.PAST_DUE:
            return PastDueSubscription(detail=detail, seq=seq, last_occurred_at=occurred_at)
        case SubscriptionStatus.CANCELED | SubscriptionStatus.EXPIRED:
            return EndedSubscription(detail=detail, status=status, seq=seq, last_occurred_at=occurred_at)
        case _:
            assert_never(status)


def subscription_detail(provider: ProviderSubscriptionData) -> SubscriptionDetail:
    return SubscriptionDetail(
        provider=provider.provider,
        external_id=provider.external_id,
        customer_id=provider.customer_id,
        user_ulid=provider.user_ulid,
        product_code=provider.product_code,
        price=provider.price,
        started_at=provider.started_at,
        current_period_end=provider.current_period_end,
        canceled_at=provider.canceled_at,
    )
