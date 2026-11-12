from dataclasses import dataclass
from datetime import datetime
from myus.utils.enum.i18n import Currency
from myus.utils.enum.payment import PaymentProvider, PayoutStatus, SubscriptionStatus, WebhookEventType
from ..data import Money


@dataclass(frozen=True, slots=True)
class ProviderSubscriptionData:
    provider: PaymentProvider
    external_id: str
    customer_id: str
    user_ulid: str
    product_code: str
    price: Money
    status: SubscriptionStatus
    started_at: datetime
    current_period_end: datetime
    canceled_at: datetime


@dataclass(frozen=True, slots=True)
class BalanceData:
    external_id: str
    amount: int
    fee: int
    currency: Currency
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class PaymentPaidContent:
    customer_id: str
    user_ulid: str
    subscription_external_id: str
    receipt_number: str
    balance: BalanceData


@dataclass(frozen=True, slots=True)
class PaymentFailedContent:
    pass


@dataclass(frozen=True, slots=True)
class RefundContent:
    balances: list[BalanceData]


@dataclass(frozen=True, slots=True)
class PayoutContent:
    amount: int
    currency: Currency
    status: PayoutStatus
    arrival_at: datetime
    balance_external_ids: list[str]


type PaymentEventContent = ProviderSubscriptionData | PaymentPaidContent | PaymentFailedContent | RefundContent | PayoutContent


@dataclass(frozen=True, slots=True)
class PaymentEventData:
    id: int
    provider: PaymentProvider
    event_id: str
    event_type: WebhookEventType
    external_id: str
    payload: str
    content: PaymentEventContent
    occurred_at: datetime
    processed_at: datetime
    attempts: int
    last_error: str
