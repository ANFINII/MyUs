from dataclasses import dataclass
from myus.domain.payment.data import Money


@dataclass(frozen=True, slots=True)
class MusicHiresData:
    id: int
    music_id: int
    file: str
    sample_rate: int
    bit_depth: int
    price: Money
