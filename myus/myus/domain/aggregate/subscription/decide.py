from datetime import datetime, timezone
from typing import assert_never
from myus.domain.aggregate.subscription.event import SubscriptionActivated, SubscriptionCancellationScheduled, SubscriptionCancellationRevoked, SubscriptionCancellationRequested, SubscriptionCancellationFailed, SubscriptionEnded, SubscriptionEvent, SubscriptionOpened, SubscriptionPaymentPastDue, SubscriptionPlanChanged, SubscriptionRenewed
from myus.domain.aggregate.subscription.state import ActiveSubscription, EndedSubscription, IncompleteSubscription, PastDueSubscription, SubscriptionDetail, SubscriptionState
from myus.domain.interface.payment.event.data import ProviderSubscriptionData
from myus.utils.common.result import Result, ValidateError, ValidationError
from myus.utils.enum.payment import CancelError, SubscriptionStatus


def accept_provider_state(state: SubscriptionState | None, provider: ProviderSubscriptionData, occurred_at: datetime) -> Result[list[SubscriptionEvent], ValidateError]:
    detail = convert_detail(provider)
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
        if detail.canceled_at == datetime.min.replace(tzinfo=timezone.utc):
            events.append(SubscriptionCancellationRevoked())
        else:
            events.append(SubscriptionCancellationScheduled(canceled_at=detail.canceled_at))
    return Result.ok(events)


def request_cancellation(state: SubscriptionState | None) -> Result[list[SubscriptionEvent], ValidateError]:
    match state:
        case ActiveSubscription() | PastDueSubscription():
            if state.detail.canceled_at != datetime.min.replace(tzinfo=timezone.utc):
                return Result.err(ValidationError("error.subscriptionNotFound"))

            if len(state.cancellation_request_id) > 0:
                return Result.ok([])

            return Result.ok([SubscriptionCancellationRequested()])
        case None | IncompleteSubscription() | EndedSubscription():
            return Result.err(ValidationError("error.subscriptionNotFound"))
        case _:
            assert_never(state)


def fail_cancellation(state: SubscriptionState | None, error: CancelError) -> Result[list[SubscriptionEvent], ValidateError]:
    match state:
        case ActiveSubscription() | PastDueSubscription():
            if len(state.cancellation_request_id) == 0:
                return Result.ok([])

            return Result.ok([SubscriptionCancellationFailed(error=error)])
        case None | IncompleteSubscription() | EndedSubscription():
            return Result.ok([])
        case _:
            assert_never(state)


def convert_detail(provider: ProviderSubscriptionData) -> SubscriptionDetail:
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
