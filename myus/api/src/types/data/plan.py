from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlanData:
    id: int
    name: str
    stripe_api_id: str
    price: int
    max_advertise: int
    description: str
