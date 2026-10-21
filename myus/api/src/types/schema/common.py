from enum import StrEnum
from typing import Annotated
from pydantic import BaseModel, Field
from api.src.domain.interface.media.index import PAGE_SIZE


class ErrorType(StrEnum):
    UNAUTHENTICATED = "UNAUTHENTICATED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION = "VALIDATION"
    INTERNAL = "INTERNAL"


class ErrorOut(BaseModel):
    type: ErrorType
    message: str


class SuccessOut(BaseModel):
    message: str


MAX_OFFSET = 10000

Limit = Annotated[int, Field(ge=1, le=PAGE_SIZE)]
Offset = Annotated[int, Field(ge=0, le=MAX_OFFSET)]
