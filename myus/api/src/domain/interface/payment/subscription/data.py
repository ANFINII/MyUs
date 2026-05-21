from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.payment.data import Money
from api.utils.enum.payment import PaymentProvider, SubscriptionStatus


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
