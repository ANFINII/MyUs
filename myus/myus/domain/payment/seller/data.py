from dataclasses import dataclass
from myus.utils.enum.payment import PaymentProvider


@dataclass(frozen=True, slots=True)
class PaymentSellerData:
    id: int
    user_id: int
    provider: PaymentProvider
    external_id: str
    is_enabled: bool
