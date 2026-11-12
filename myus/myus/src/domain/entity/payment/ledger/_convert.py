from myus.db.models.payment import PaymentLedgerEntry
from myus.src.domain.interface.payment.ledger.data import LedgerEntryData
from myus.utils.enum.payment import LedgerEntryType


def convert_data(obj: PaymentLedgerEntry) -> LedgerEntryData:
    return LedgerEntryData(
        id=obj.id,
        transaction_id=obj.transaction_id,
        payout_id=obj.payout_id or 0,
        event_id=obj.event_id,
        external_id=obj.external_id,
        entry_type=LedgerEntryType(obj.entry_type),
        amount=obj.amount,
        tax_amount=obj.tax_amount,
        occurred_at=obj.occurred_at,
    )


def marshal_data(data: LedgerEntryData) -> PaymentLedgerEntry:
    return PaymentLedgerEntry(
        id=data.id if data.id != 0 else None,
        transaction_id=data.transaction_id,
        payout_id=data.payout_id if data.payout_id != 0 else None,
        event_id=data.event_id,
        external_id=data.external_id,
        entry_type=data.entry_type,
        amount=data.amount,
        tax_amount=data.tax_amount,
        occurred_at=data.occurred_at,
    )
