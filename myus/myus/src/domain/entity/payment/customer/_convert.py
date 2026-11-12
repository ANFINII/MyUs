from myus.db.models.payment import PaymentCustomer
from myus.src.domain.interface.payment.customer.data import PaymentCustomerData
from myus.utils.enum.payment import PaymentProvider


def convert_data(obj: PaymentCustomer) -> PaymentCustomerData:
    return PaymentCustomerData(
        id=obj.id,
        user_id=obj.user_id,
        provider=PaymentProvider(obj.provider),
        external_id=obj.external_id,
    )


def marshal_data(data: PaymentCustomerData) -> PaymentCustomer:
    return PaymentCustomer(
        id=data.id if data.id != 0 else None,
        user_id=data.user_id,
        provider=data.provider,
        external_id=data.external_id,
    )
