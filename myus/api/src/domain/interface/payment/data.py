from dataclasses import dataclass
from datetime import datetime
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import PaymentProvider, PaymentStatus, SubscriptionStatus


@dataclass(frozen=True, slots=True)
class Money:
    amount: int
    currency: Currency


@dataclass(frozen=True, slots=True)
class SubscriptionData:
    id: int
    customer_user_id: int
    seller_id: str
    provider: PaymentProvider
    external_id: str
    product_code: str
    price: Money
    status: SubscriptionStatus
    started_at: datetime
    current_period_end: datetime
    canceled_at: datetime


@dataclass(frozen=True, slots=True)
class PaymentTransactionData:
    id: int
    subscription_id: int
    customer_user_id: int
    provider: PaymentProvider
    external_id: str
    price: Money
    status: PaymentStatus
    paid_at: datetime
