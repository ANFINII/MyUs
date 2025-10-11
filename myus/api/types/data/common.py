from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ErrorData:
    code: int
    message: str
