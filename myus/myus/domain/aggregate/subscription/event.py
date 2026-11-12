from dataclasses import dataclass
from datetime import datetime
from typing import Any
from myus.domain.aggregate.subscription.state import SubscriptionDetail
from myus.domain.payment.data import Money
from myus.utils.enum.payment import CancelError, PaymentProvider, SubscriptionStatus


SUBSCRIPTION_AGGREGATE_TYPE = "Subscription"


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
class SubscriptionCancellationRevoked:
    pass


@dataclass(frozen=True, slots=True)
class SubscriptionCancellationRequested:
    pass


@dataclass(frozen=True, slots=True)
class SubscriptionCancellationFailed:
    error: CancelError


@dataclass(frozen=True, slots=True)
class SubscriptionEnded:
    status: SubscriptionStatus
    canceled_at: datetime


type SubscriptionEvent = SubscriptionOpened | SubscriptionActivated | SubscriptionRenewed | SubscriptionPlanChanged | SubscriptionPaymentPastDue | SubscriptionCancellationScheduled | SubscriptionCancellationRevoked | SubscriptionCancellationRequested | SubscriptionCancellationFailed | SubscriptionEnded


SUBSCRIPTION_EVENT_CLASSES: dict[str, type[Any]] = {
    "Subscription.Opened.V1": SubscriptionOpened,
    "Subscription.Activated.V1": SubscriptionActivated,
    "Subscription.Renewed.V1": SubscriptionRenewed,
    "Subscription.PlanChanged.V1": SubscriptionPlanChanged,
    "Subscription.PaymentPastDue.V1": SubscriptionPaymentPastDue,
    "Subscription.CancellationScheduled.V1": SubscriptionCancellationScheduled,
    "Subscription.CancellationRevoked.V1": SubscriptionCancellationRevoked,
    "Subscription.CancellationRequested.V1": SubscriptionCancellationRequested,
    "Subscription.CancellationFailed.V1": SubscriptionCancellationFailed,
    "Subscription.Ended.V1": SubscriptionEnded,
}


def subscription_aggregate_id(provider: PaymentProvider, external_id: str) -> str:
    return f"{provider.value}:{external_id}"
