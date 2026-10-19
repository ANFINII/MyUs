from __future__ import annotations

from dataclasses import dataclass
from typing import Self, final


@dataclass(frozen=True)
class AnyError:
    """Result型のE型パラメータに使うための基底エラー型"""

    error_message: str

    @classmethod
    def from_exception(cls, exception: Exception) -> Self:
        return cls(repr(exception))


@final
@dataclass(frozen=True)
class FatalError(AnyError):
    pass


@final
@dataclass(frozen=True)
class UnauthorizedError(AnyError):
    pass


@final
@dataclass(frozen=True)
class NotFoundError(AnyError):
    pass
