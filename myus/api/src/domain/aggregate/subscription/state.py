from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.payment.data import Money
from api.utils.enum.payment import PaymentProvider, SubscriptionStatus


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


@dataclass(frozen=True, slots=True)
class PastDueSubscription:
    detail: SubscriptionDetail
    seq: int
    last_occurred_at: datetime


@dataclass(frozen=True, slots=True)
class EndedSubscription:
    detail: SubscriptionDetail
    status: SubscriptionStatus
    seq: int
    last_occurred_at: datetime


type SubscriptionState = IncompleteSubscription | ActiveSubscription | PastDueSubscription | EndedSubscription
