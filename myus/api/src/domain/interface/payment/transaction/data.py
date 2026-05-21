from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.payment.data import Money
from api.utils.enum.payment import PaymentProvider, PaymentStatus


@dataclass(frozen=True, slots=True)
class TransactionData:
    id: int
    subscription_id: int
    customer_user_id: int
    provider: PaymentProvider
    external_id: str
    price: Money
    status: PaymentStatus
    paid_at: datetime
