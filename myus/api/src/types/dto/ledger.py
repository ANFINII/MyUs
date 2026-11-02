from dataclasses import dataclass
from datetime import datetime
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import LedgerEntryType, PaymentProvider


@dataclass(frozen=True, slots=True)
class LedgerRowDTO:
    occurred_at: datetime
    provider: PaymentProvider
    entry_type: LedgerEntryType
    amount: int
    tax_amount: int
    currency: Currency
    transaction_external_id: str
    receipt_number: str
    payout_external_id: str
    payout_arrival_at: datetime | None
