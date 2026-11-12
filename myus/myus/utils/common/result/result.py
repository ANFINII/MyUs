from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import cast

from myus.modules.logger import log

from .errors import AnyError, FatalError


class _Nil:
    """Result の nil 状態を表す内部クラス。
    is_ok の場合は err_value が _Nil、is_err の場合は ok_value が _Nil。
    None と区別するために専用クラスを用意している。
    """


class Result[T, E: AnyError]:
    """Rust の Result<T, E> 相当の公開クラス。
    E は AnyError 派生に限定する。
    """

    def __init__(self, *, is_ok: bool, ok_value: T | _Nil, err_value: E | _Nil) -> None:
        self._is_ok = is_ok
        self._ok_value = ok_value
        self._err_value = err_value

    def __repr__(self) -> str:
        if self.is_ok:
            return f"Result[ok={self.ok_value}]"
        return f"Result[err={self.err_value}]"

    __str__ = __repr__

    @classmethod
    def ok(cls, value: T) -> Result[T, E]:
        return Result(is_ok=True, ok_value=value, err_value=_Nil())

    @classmethod
    def err(cls, message: E) -> Result[T, E]:
        return Result(is_ok=False, ok_value=_Nil(), err_value=message)

    @classmethod
    def shield_exception[R, F: AnyError, **P](cls) -> Callable[[Callable[P, Result[R, F]]], Callable[P, Result[R, F | FatalError]]]:
        """関数内の例外を捕捉して FatalError を含む Result に変換するデコレータ"""

        def decorator(func: Callable[P, Result[R, F]]) -> Callable[P, Result[R, F | FatalError]]:
            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, F | FatalError]:
                try:
                    return cast(Result[R, F | FatalError], func(*args, **kwargs))
                except Exception as err:
                    log.error("Unhandled Exception Occurred!", exc=err)
                    return Result.err(FatalError.from_exception(err))

            return wrapper

        return decorator

    @property
    def is_ok(self) -> bool:
        return self._is_ok

    @property
    def is_err(self) -> bool:
        return not self._is_ok

    @property
    def ok_value(self) -> T:
        if not self._is_ok:
            raise RuntimeError("結果がerrの場合はok_valueにアクセスしないでください")
        assert not isinstance(self._ok_value, _Nil)
        return self._ok_value

    @property
    def err_value(self) -> E:
        if self._is_ok:
            raise RuntimeError("結果がokの場合はerr_valueにアクセスしないでください")
        assert not isinstance(self._err_value, _Nil)
        return self._err_value
