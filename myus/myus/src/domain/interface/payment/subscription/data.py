from dataclasses import dataclass
from datetime import datetime
from myus.src.domain.interface.payment.data import Money
from myus.utils.enum.payment import SubscriptionStatus


@dataclass(frozen=True, slots=True)
class SubscriptionData:
    id: int
    payment_customer_id: int
    seller_id: str
    external_id: str
    product_code: str
    price: Money
    status: SubscriptionStatus
    started_at: datetime
    current_period_end: datetime
    canceled_at: datetime
    last_event_at: datetime
