from __future__ import annotations

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class AnyError:
    """Result型のE型パラメータに使うための基底エラー型"""

    error_message: str

    @classmethod
    def from_exception(cls, exception: Exception) -> Self:
        return cls(repr(exception))


@dataclass(frozen=True)
class FatalError(AnyError):
    pass


@dataclass(frozen=True)
class UnauthorizedError(AnyError):
    pass
