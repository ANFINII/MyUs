from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SellerDTO:
    is_available: bool
    is_registered: bool
    is_enabled: bool
