from dataclasses import dataclass
from datetime import datetime
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import PaymentStatus


@dataclass(frozen=True, slots=True)
class TransactionData:
    id: int
    payment_customer_id: int
    subscription_id: int
    external_id: str
    currency: Currency
    tax_rate: int
    receipt_number: str
    status: PaymentStatus
    paid_at: datetime
    last_event_at: datetime
