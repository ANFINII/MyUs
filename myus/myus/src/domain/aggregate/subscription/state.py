from dataclasses import dataclass
from datetime import datetime
from typing import assert_never
from myus.src.domain.interface.payment.data import Money
from myus.utils.enum.payment import PaymentProvider, SubscriptionStatus


@dataclass(frozen=True, slots=True)
class SubscriptionDetail:
    provider: PaymentProvider
    external_id: str
    customer_id: str
    user_ulid: str
    product_code: str
    price: Money
    started_at: datetime
    current_period_end: datetime
    canceled_at: datetime


@dataclass(frozen=True, slots=True)
class IncompleteSubscription:
    detail: SubscriptionDetail
    seq: int
    last_occurred_at: datetime


@dataclass(frozen=True, slots=True)
class ActiveSubscription:
    detail: SubscriptionDetail
    seq: int
    last_occurred_at: datetime
    cancellation_request_id: str


@dataclass(frozen=True, slots=True)
class PastDueSubscription:
    detail: SubscriptionDetail
    seq: int
    last_occurred_at: datetime
    cancellation_request_id: str


@dataclass(frozen=True, slots=True)
class EndedSubscription:
    detail: SubscriptionDetail
    status: SubscriptionStatus
    seq: int
    last_occurred_at: datetime


type SubscriptionState = IncompleteSubscription | ActiveSubscription | PastDueSubscription | EndedSubscription


def convert_status(state: SubscriptionState) -> SubscriptionStatus:
    match state:
        case IncompleteSubscription():
            return SubscriptionStatus.INCOMPLETE
        case ActiveSubscription():
            return SubscriptionStatus.ACTIVE
        case PastDueSubscription():
            return SubscriptionStatus.PAST_DUE
        case EndedSubscription(status=status):
            return status
        case _:
            assert_never(state)
