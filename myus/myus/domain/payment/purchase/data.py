from dataclasses import dataclass
from myus.utils.enum.payment import ProductType


@dataclass(frozen=True, slots=True)
class PurchaseData:
    id: int
    user_id: int
    transaction_id: int
    product_type: ProductType
    product_id: int
