from myus.db.models.payment import Purchase
from myus.domain.payment.purchase.data import PurchaseData
from myus.utils.enum.payment import ProductType


def convert_data(obj: Purchase) -> PurchaseData:
    return PurchaseData(
        id=obj.id,
        user_id=obj.user_id,
        transaction_id=obj.transaction_id,
        product_type=ProductType(obj.product_type),
        product_id=obj.product_id,
    )


def marshal_data(data: PurchaseData) -> Purchase:
    return Purchase(
        id=data.id if data.id != 0 else None,
        user_id=data.user_id,
        transaction_id=data.transaction_id,
        product_type=data.product_type,
        product_id=data.product_id,
    )
