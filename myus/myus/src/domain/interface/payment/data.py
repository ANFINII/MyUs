from dataclasses import dataclass
from myus.utils.enum.i18n import Currency


@dataclass(frozen=True, slots=True)
class Money:
    amount: int
    currency: Currency
