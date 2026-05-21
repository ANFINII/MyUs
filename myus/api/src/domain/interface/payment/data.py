from dataclasses import dataclass
from datetime import datetime
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import PaymentProvider, PaymentStatus


@dataclass(frozen=True, slots=True)
class Money:
    amount: int
    currency: Currency


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
