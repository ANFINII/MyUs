from dataclasses import dataclass
from datetime import datetime
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import PaymentProvider, PayoutStatus


@dataclass(frozen=True, slots=True)
class PayoutData:
    id: int
    provider: PaymentProvider
    external_id: str
    amount: int
    currency: Currency
    status: PayoutStatus
    arrival_at: datetime
    last_event_at: datetime
