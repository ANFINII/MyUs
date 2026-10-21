from enum import StrEnum
from pydantic import BaseModel


class ErrorType(StrEnum):
    UNAUTHENTICATED = "UNAUTHENTICATED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION = "VALIDATION"
    INTERNAL = "INTERNAL"


class ErrorOut(BaseModel):
    type: ErrorType | None = None
    message: str
