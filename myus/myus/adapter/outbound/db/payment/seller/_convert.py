from myus.db.models.payment import PaymentSeller
from myus.domain.payment.seller.data import PaymentSellerData
from myus.utils.enum.payment import PaymentProvider


def convert_data(obj: PaymentSeller) -> PaymentSellerData:
    return PaymentSellerData(
        id=obj.id,
        user_id=obj.user_id,
        provider=PaymentProvider(obj.provider),
        external_id=obj.external_id,
        is_enabled=obj.is_enabled,
    )


def marshal_data(data: PaymentSellerData) -> PaymentSeller:
    return PaymentSeller(
        id=data.id if data.id != 0 else None,
        user_id=data.user_id,
        provider=data.provider,
        external_id=data.external_id,
        is_enabled=data.is_enabled,
    )
