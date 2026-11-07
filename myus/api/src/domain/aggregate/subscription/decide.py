from datetime import datetime
from typing import assert_never
from api.src.domain.aggregate.subscription.event import SubscriptionActivated, SubscriptionCancellationScheduled, SubscriptionEnded, SubscriptionEvent, SubscriptionOpened, SubscriptionPaymentPastDue, SubscriptionPlanChanged, SubscriptionRenewed
from api.src.domain.aggregate.subscription.state import ActiveSubscription, EndedSubscription, IncompleteSubscription, PastDueSubscription, SubscriptionDetail, SubscriptionState
from api.src.domain.interface.payment.event.data import ProviderSubscriptionData
from api.utils.common.result import Result, ValidateError
from api.utils.enum.payment import SubscriptionStatus


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
        events.append(SubscriptionCancellationScheduled(canceled_at=detail.canceled_at))
    return Result.ok(events)


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
