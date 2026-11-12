from dataclasses import dataclass
from datetime import datetime
from myus.utils.enum.payment import LedgerEntryType


@dataclass(frozen=True, slots=True)
class LedgerEntryData:
    id: int
    transaction_id: int
    payout_id: int
    event_id: int
    external_id: str
    entry_type: LedgerEntryType
    amount: int
    tax_amount: int
    occurred_at: datetime
