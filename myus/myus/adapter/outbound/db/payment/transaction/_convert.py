from myus.db.models.payment import PaymentTransaction
from myus.domain.interface.payment.transaction.data import TransactionData
from myus.utils.enum.i18n import Currency
from myus.utils.enum.payment import PaymentStatus


def convert_data(obj: PaymentTransaction) -> TransactionData:
    return TransactionData(
        id=obj.id,
        payment_customer_id=obj.payment_customer_id,
        subscription_id=obj.subscription_id or 0,
        external_id=obj.external_id,
        currency=Currency(obj.currency),
        tax_rate=obj.tax_rate,
        receipt_number=obj.receipt_number,
        status=PaymentStatus(obj.status),
        paid_at=obj.paid_at,
        last_event_at=obj.last_event_at,
    )


def marshal_data(data: TransactionData) -> PaymentTransaction:
    return PaymentTransaction(
        id=data.id if data.id != 0 else None,
        payment_customer_id=data.payment_customer_id,
        subscription_id=data.subscription_id if data.subscription_id != 0 else None,
        external_id=data.external_id,
        currency=data.currency,
        tax_rate=data.tax_rate,
        receipt_number=data.receipt_number,
        status=data.status,
        paid_at=data.paid_at,
        last_event_at=data.last_event_at,
    )
