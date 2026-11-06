from dataclasses import replace
from datetime import datetime, timezone
from itertools import permutations
from api.src.domain.aggregate.subscription.aggregate import accept_provider_state, apply_subscription, replay_subscription
from api.src.domain.aggregate.subscription.data import ActiveSubscription, EndedSubscription, PastDueSubscription, SubscriptionActivated, SubscriptionEvent, SubscriptionState
from api.src.domain.interface.es.data import EventEnvelope
from api.src.domain.interface.payment.event.data import ProviderSubscriptionData
from api.tests.fakes import provider_subscription
from api.utils.common.result import HistoryCorruptedError
from api.utils.enum.payment import SubscriptionStatus
from api.utils.enum.user import PlanName
from api.utils.functions.es import new_event_id


AGGREGATE_ID = "01SUBSCRIPTION"
PERIOD_1 = datetime(2026, 11, 1, tzinfo=timezone.utc)
PERIOD_2 = datetime(2026, 12, 1, tzinfo=timezone.utc)
CANCELED_AT = datetime(2026, 11, 15, tzinfo=timezone.utc)


def at(day: int) -> datetime:
    return datetime(2026, 10, day, tzinfo=timezone.utc)


def provider(status: SubscriptionStatus, period_end: datetime = PERIOD_1, plan: str = PlanName.PREMIUM, canceled_at: datetime = datetime.min.replace(tzinfo=timezone.utc)) -> ProviderSubscriptionData:
    return replace(provider_subscription("sub_1", "01USER", plan, status), current_period_end=period_end, canceled_at=canceled_at)


def envelope(seq: int, event: SubscriptionEvent, occurred_at: datetime) -> EventEnvelope[SubscriptionEvent]:
    return EventEnvelope(event_id=new_event_id("Subscription", AGGREGATE_ID, seq), aggregate_type="Subscription", aggregate_id=AGGREGATE_ID, seq=seq, occurred_at=occurred_at, event=event)


def accept_all(facts: list[tuple[ProviderSubscriptionData, datetime]]) -> tuple[SubscriptionState | None, list[EventEnvelope[SubscriptionEvent]]]:
    history: list[EventEnvelope[SubscriptionEvent]] = []
    state: SubscriptionState | None = None
    for fact, occurred_at in facts:
        events_ret = accept_provider_state(state, fact, occurred_at)
        assert events_ret.is_ok, events_ret
        for event in events_ret.ok_value:
            history.append(envelope(len(history) + 1, event, occurred_at))
            apply_ret = apply_subscription(state, history[-1])
            assert apply_ret.is_ok, apply_ret
            state = apply_ret.ok_value

    return state, history


def test_lifecycle_produces_only_needed_events() -> None:
    state, history = accept_all([
        (provider(SubscriptionStatus.INCOMPLETE), at(1)),
        (provider(SubscriptionStatus.ACTIVE), at(2)),
        (provider(SubscriptionStatus.ACTIVE), at(3)),
        (provider(SubscriptionStatus.PAST_DUE, PERIOD_2), at(4)),
        (provider(SubscriptionStatus.ACTIVE, PERIOD_2, PlanName.BASIC), at(5)),
        (provider(SubscriptionStatus.ACTIVE, PERIOD_2, PlanName.BASIC, CANCELED_AT), at(6)),
        (provider(SubscriptionStatus.CANCELED, PERIOD_2, PlanName.BASIC, CANCELED_AT), at(7)),
    ])

    assert [type(e.event).__name__ for e in history] == [
        "SubscriptionOpened",
        "SubscriptionActivated",
        "SubscriptionRenewed",
        "SubscriptionPaymentPastDue",
        "SubscriptionPlanChanged",
        "SubscriptionActivated",
        "SubscriptionCancellationScheduled",
        "SubscriptionEnded",
    ]
    assert isinstance(state, EndedSubscription)
    assert state.status == SubscriptionStatus.CANCELED
    assert state.detail.product_code == PlanName.BASIC
    assert state.detail.current_period_end == PERIOD_2
    assert state.detail.canceled_at == CANCELED_AT
    replay_ret = replay_subscription(history)
    assert replay_ret.is_ok, replay_ret
    assert replay_ret.ok_value == state


def test_arrival_order_does_not_change_final_state() -> None:
    facts = [
        (provider(SubscriptionStatus.INCOMPLETE), at(1)),
        (provider(SubscriptionStatus.ACTIVE), at(2)),
        (provider(SubscriptionStatus.PAST_DUE), at(3)),
        (provider(SubscriptionStatus.ACTIVE, PERIOD_2), at(4)),
    ]

    final_states = set()
    for order in permutations(facts):
        state, _ = accept_all(list(order))
        assert isinstance(state, ActiveSubscription)
        final_states.add(state.detail)

    assert len(final_states) == 1
    assert final_states.pop().current_period_end == PERIOD_2


def test_canceled_wins_over_active_at_same_time() -> None:
    facts = [(provider(SubscriptionStatus.ACTIVE), at(2)), (provider(SubscriptionStatus.CANCELED, canceled_at=CANCELED_AT), at(2))]

    for order in permutations(facts):
        state, _ = accept_all(list(order))
        assert isinstance(state, EndedSubscription)


def test_same_state_is_no_op() -> None:
    state, _ = accept_all([(provider(SubscriptionStatus.ACTIVE), at(1))])

    ret = accept_provider_state(state, provider(SubscriptionStatus.ACTIVE), at(2))

    assert ret.is_ok, ret
    assert ret.ok_value == []


def test_past_due_after_incomplete_activates_first() -> None:
    state, history = accept_all([(provider(SubscriptionStatus.INCOMPLETE), at(1)), (provider(SubscriptionStatus.PAST_DUE), at(2))])

    assert isinstance(state, PastDueSubscription)
    assert [type(e.event).__name__ for e in history] == ["SubscriptionOpened", "SubscriptionActivated", "SubscriptionPaymentPastDue"]


def test_event_not_acceptable_in_state_is_history_corrupted() -> None:
    state, _ = accept_all([(provider(SubscriptionStatus.CANCELED), at(1))])

    ret = apply_subscription(state, envelope(2, SubscriptionActivated(current_period_end=PERIOD_1), at(2)))

    assert ret.is_err
    assert isinstance(ret.err_value, HistoryCorruptedError)


def test_seq_gap_is_history_corrupted() -> None:
    state, _ = accept_all([(provider(SubscriptionStatus.ACTIVE), at(1))])

    ret = apply_subscription(state, envelope(3, SubscriptionActivated(current_period_end=PERIOD_1), at(2)))

    assert ret.is_err
    assert isinstance(ret.err_value, HistoryCorruptedError)
