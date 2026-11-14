from dataclasses import dataclass
from myus.domain.payment.data import Money


@dataclass(frozen=True, slots=True)
class PlanPriceDTO:
    name: str
    price: Money
