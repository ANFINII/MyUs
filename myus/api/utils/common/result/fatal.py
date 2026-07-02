from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, assert_never

from ._log import LogLevel, emit_log
from ._result import _Result
from ._result_err_base import ResultErrBase
from .errors import FatalError


class ResultFatal[T](ResultErrBase[T, FatalError]):
    """E を FatalError に固定した Result。
    エラー型を分岐させたくない場面 (致命的エラーとしてまとめて扱う場面) で使う。
    """

    @classmethod
    def ok(cls, value: T) -> ResultFatal[T]:
        return ResultFatal(_Result.ok(value))

    @classmethod
    def _err(
        cls,
        message: str | FatalError | Exception | ResultFatal[Any],
        *,
        loglevel: LogLevel | None,
        **kwargs: Any,
    ) -> ResultFatal[T]:
        if loglevel is not None:
            emit_log(loglevel, str(message), err_from=repr(message), **kwargs)

        match message:
            case FatalError():
                return ResultFatal(_Result.err(message))
            case str():
                return ResultFatal(_Result.err(FatalError(message)))
            case Exception():
                return ResultFatal(_Result.err(FatalError.from_exception(message)))
            case ResultFatal():
                return ResultFatal(_Result.err(message.err_value))
            case _:
                assert_never(message)

    @classmethod
    def new(cls, message: str | FatalError | Exception | ResultFatal[Any]) -> ResultFatal[T]:
        return cls._err(message, loglevel=None)

    @classmethod
    def shield_exception[R, **P](
        cls,
        *,
        loglevel: LogLevel = "error",
    ) -> Callable[[Callable[P, ResultFatal[R]]], Callable[P, ResultFatal[R]]]:
        def decorator(func: Callable[P, ResultFatal[R]]) -> Callable[P, ResultFatal[R]]:
            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> ResultFatal[R]:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    exc: Any = err if loglevel == "error" else repr(err)
                    emit_log(loglevel, "Unhandled Exception Occurred!", exc=exc)
                    return ResultFatal._err(err, loglevel=None)

            return wrapper

        return decorator

    @classmethod
    def error(
        cls,
        message: str | FatalError | Exception | ResultFatal[Any],
        **kwargs: Any,
    ) -> ResultFatal[T]:
        return cls._err(message, loglevel="error", **kwargs)

    @classmethod
    def warning(
        cls,
        message: str | FatalError | Exception | ResultFatal[Any],
        **kwargs: Any,
    ) -> ResultFatal[T]:
        return cls._err(message, loglevel="warning", **kwargs)

    @classmethod
    def info(
        cls,
        message: str | FatalError | Exception | ResultFatal[Any],
        **kwargs: Any,
    ) -> ResultFatal[T]:
        return cls._err(message, loglevel="info", **kwargs)

    @classmethod
    def debug(
        cls,
        message: str | FatalError | Exception | ResultFatal[Any],
        **kwargs: Any,
    ) -> ResultFatal[T]:
        return cls._err(message, loglevel="debug", **kwargs)

    def _type_name(self) -> str:
        return "ResultFatal"
