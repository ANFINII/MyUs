from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BlogPurchaseData:
    id: int
    user_id: int
    blog_id: int
    transaction_id: int
