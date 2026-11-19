from django_ulid.models import ulid
from myus.db.models.payment import Product
from myus.domain.payment.data import Money
from myus.domain.payment.product.data import ProductData
from myus.utils.enum.i18n import Currency
from myus.utils.enum.payment import ProductType


def convert_data(obj: Product) -> ProductData:
    return ProductData(
        id=obj.id,
        ulid=obj.ulid,
        seller_id=obj.seller_id,
        product_type=ProductType(obj.product_type),
        object_id=obj.object_id,
        price=Money(amount=obj.price, currency=Currency(obj.currency)),
    )


def marshal_data(data: ProductData) -> Product:
    return Product(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        seller_id=data.seller_id,
        product_type=data.product_type,
        object_id=data.object_id,
        price=data.price.amount,
        currency=data.price.currency,
    )
