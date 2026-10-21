from enum import StrEnum
from pydantic import BaseModel


class ErrorOut(BaseModel):
    message: str


class ErrorType(StrEnum):
    UNAUTHENTICATED = "UNAUTHENTICATED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION = "VALIDATION"
    INTERNAL = "INTERNAL"


class ProblemOut(BaseModel):
    type: ErrorType
    message: str
