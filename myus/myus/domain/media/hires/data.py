from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AudioHiresData:
    id: int
    audio_id: int
    file: str
    sample_rate: int
    bit_depth: int
