from dataclasses import dataclass
from datetime import datetime
from typing import Any
from api.src.domain.interface.payment.data import Money
from api.utils.enum.payment import PaymentProvider, SubscriptionStatus


SUBSCRIPTION_AGGREGATE_TYPE = "Subscription"


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


@dataclass(frozen=True, slots=True)
class SubscriptionOpened:
    detail: SubscriptionDetail
    status: SubscriptionStatus


@dataclass(frozen=True, slots=True)
class SubscriptionActivated:
    current_period_end: datetime


@dataclass(frozen=True, slots=True)
class SubscriptionRenewed:
    current_period_end: datetime


@dataclass(frozen=True, slots=True)
class SubscriptionPlanChanged:
    product_code: str
    price: Money


@dataclass(frozen=True, slots=True)
class SubscriptionPaymentPastDue:
    pass


@dataclass(frozen=True, slots=True)
class SubscriptionCancellationScheduled:
    canceled_at: datetime


@dataclass(frozen=True, slots=True)
class SubscriptionEnded:
    status: SubscriptionStatus
    canceled_at: datetime


type SubscriptionEvent = SubscriptionOpened | SubscriptionActivated | SubscriptionRenewed | SubscriptionPlanChanged | SubscriptionPaymentPastDue | SubscriptionCancellationScheduled | SubscriptionEnded


SUBSCRIPTION_EVENT_CLASSES: dict[str, type[Any]] = {
    "Subscription.Opened.V1": SubscriptionOpened,
    "Subscription.Activated.V1": SubscriptionActivated,
    "Subscription.Renewed.V1": SubscriptionRenewed,
    "Subscription.PlanChanged.V1": SubscriptionPlanChanged,
    "Subscription.PaymentPastDue.V1": SubscriptionPaymentPastDue,
    "Subscription.CancellationScheduled.V1": SubscriptionCancellationScheduled,
    "Subscription.Ended.V1": SubscriptionEnded,
}
