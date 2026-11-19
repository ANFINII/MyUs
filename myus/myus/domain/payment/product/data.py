from dataclasses import dataclass
from myus.utils.enum.payment import ProductType
from ..data import Money


@dataclass(frozen=True, slots=True)
class ProductData:
    id: int
    ulid: str
    seller_id: int
    product_type: ProductType
    object_id: int
    price: Money
