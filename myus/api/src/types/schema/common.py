from enum import StrEnum
from typing import Literal
from pydantic import BaseModel


class ErrorType(StrEnum):
    UNAUTHENTICATED = "UNAUTHENTICATED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION = "VALIDATION"
    INTERNAL = "INTERNAL"


class ErrorOut(BaseModel):
    status: Literal[400, 500]
    type: ErrorType
    message: str


class SuccessOut(BaseModel):
    message: str
