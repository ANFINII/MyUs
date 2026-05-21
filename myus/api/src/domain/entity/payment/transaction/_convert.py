from api.db.models.payment import PaymentTransaction
from api.src.domain.interface.payment.data import Money
from api.src.domain.interface.payment.transaction.data import TransactionData
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import PaymentProvider, PaymentStatus


def convert_data(obj: PaymentTransaction) -> TransactionData:
    return TransactionData(
        id=obj.id,
        subscription_id=obj.subscription_id,
        customer_user_id=obj.customer_id,
        provider=PaymentProvider(obj.provider),
        external_id=obj.external_id,
        price=Money(amount=obj.price_amount, currency=Currency(obj.price_currency)),
        status=PaymentStatus(obj.status),
        paid_at=obj.paid_at,
    )


def marshal_data(data: TransactionData) -> PaymentTransaction:
    return PaymentTransaction(
        id=data.id if data.id != 0 else None,
        subscription_id=data.subscription_id,
        customer_id=data.customer_user_id,
        provider=data.provider,
        external_id=data.external_id,
        price_amount=data.price.amount,
        price_currency=data.price.currency,
        status=data.status,
        paid_at=data.paid_at,
    )
