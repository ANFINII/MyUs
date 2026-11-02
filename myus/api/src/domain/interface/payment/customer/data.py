from dataclasses import dataclass
from api.utils.enum.payment import PaymentProvider


@dataclass(frozen=True, slots=True)
class PaymentCustomerData:
    id: int
    user_id: int
    provider: PaymentProvider
    external_id: str
