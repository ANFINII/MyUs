from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlanData:
    name: str
    stripe_api_id: str
    price: str
    max_advertise: int
    description: int
