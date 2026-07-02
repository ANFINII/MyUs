from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import cast

from ._result import _Result


class ResultErrBase[T, E](ABC):
    """Result系クラスの共通基底。
    Result / ResultFatal はこのクラスを継承して E 型を絞り込む。
    """

    def __init__(self, result: _Result[T, E]) -> None:
        self._result = result

    @abstractmethod
    def _type_name(self) -> str:
        ...

    def __repr__(self) -> str:
        if self.is_ok:
            return f"{self._type_name()}[ok={self.ok_value}]"
        return f"{self._type_name()}[err={self.err_value}]"

    __str__ = __repr__

    def maybe_ok(self) -> T | None:
        return self._result.maybe_ok()

    def maybe_err(self) -> E | None:
        return self._result.maybe_err()

    @property
    def is_ok(self) -> bool:
        return self._result.is_ok

    @property
    def is_err(self) -> bool:
        return self._result.is_err

    @property
    def ok_value(self) -> T:
        return self._result.ok_value

    @property
    def err_value(self) -> E:
        return self._result.err_value

    def map[U](self, f: Callable[[T], U]) -> ResultErrBase[U, E]:
        return cast(ResultErrBase[U, E], self.__class__(cast(_Result[T, E], self._result.map(f))))

    def map_err(self, f: Callable[[E], E]) -> ResultErrBase[T, E]:
        return self.__class__(self._result.map_err(f))

    def and_then[U](self, f: Callable[[T], ResultErrBase[U, E]]) -> ResultErrBase[U, E]:
        if self.is_ok:
            return f(self.ok_value)
        return cast(ResultErrBase[U, E], self)

    def ok_value_or(self, default: T) -> T:
        return self._result.ok_value_or(default)

    def ok_value_or_else(self, f: Callable[[E], T]) -> T:
        return self._result.ok_value_or_else(f)

    def expect(self, msg: str) -> T:
        return self._result.expect(msg)
