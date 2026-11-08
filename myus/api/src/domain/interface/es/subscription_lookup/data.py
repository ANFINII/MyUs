from dataclasses import dataclass
from api.utils.enum.payment import PaymentProvider


@dataclass(frozen=True, slots=True)
class SubscriptionLookupData:
    id: int
    aggregate_id: str
    provider: PaymentProvider
    external_id: str
