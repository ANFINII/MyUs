from dataclasses import dataclass
from myus.utils.enum.i18n import Currency


@dataclass(frozen=True, slots=True)
class SellerDTO:
    is_available: bool
    is_registered: bool
    is_enabled: bool
    currency: Currency
