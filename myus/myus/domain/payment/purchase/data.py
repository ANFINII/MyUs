from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PurchaseData:
    id: int
    user_id: int
    product_id: int
    transaction_id: int
