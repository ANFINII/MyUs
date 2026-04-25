from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NgWordData:
    id: int
    word: str
