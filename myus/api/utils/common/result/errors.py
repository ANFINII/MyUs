from __future__ import annotations

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class AnyError:
    """Result型のE型パラメータに使うための基底エラー型"""

    message: str

    @classmethod
    def from_exception(cls, exception: Exception) -> Self:
        return cls(repr(exception))


@dataclass(frozen=True)
class FatalError(AnyError):
    pass


@dataclass(frozen=True)
class UnauthorizedError(AnyError):
    pass


@dataclass(frozen=True)
class NotFoundError(AnyError):
    pass


@dataclass(frozen=True)
class ForbiddenError(AnyError):
    pass


@dataclass(frozen=True)
class ValidationError(AnyError):
    pass


@dataclass(frozen=True)
class ConflictError(AnyError):
    pass


@dataclass(frozen=True)
class HistoryCorruptedError(AnyError):
    pass


type FindError = NotFoundError | FatalError
type AccessError = NotFoundError | ForbiddenError | FatalError
type InputError = NotFoundError | ValidationError | FatalError
type WriteError = NotFoundError | ForbiddenError | ValidationError | FatalError
type ValidateError = ValidationError | FatalError
type HistoryError = HistoryCorruptedError | FatalError
type AppendError = ConflictError | FatalError
type CommandError = ValidationError | ConflictError | HistoryCorruptedError | FatalError
