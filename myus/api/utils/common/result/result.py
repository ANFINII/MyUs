from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, cast

from ._log import LogLevel, emit_log
from ._result import _Result
from ._result_err_base import ResultErrBase
from .errors import AnyError, FatalError


class Result[T, E: AnyError](ResultErrBase[T, E]):
    """Rust の Result<T, E> 相当の公開クラス。
    E は AnyError 派生に限定する。エラー時にログ出力するヘルパも提供する。
    """

    @classmethod
    def ok(cls, value: T) -> Result[T, E]:
        return Result(_Result.ok(value))

    @classmethod
    def _err(
        cls,
        message: E | Result[T, E],
        *,
        loglevel: LogLevel | None,
        log_message_body: str | None,
        **kwargs: Any,
    ) -> Result[T, E]:
        if loglevel is not None:
            body = log_message_body if log_message_body is not None else str(message)
            emit_log(loglevel, body, err_from=repr(message), **kwargs)

        if isinstance(message, Result):
            return Result(_Result.err(message.err_value))
        return Result(_Result.err(message))

    @classmethod
    def new(cls, message: E | Result[T, E]) -> Result[T, E]:
        """Err を生成するファクトリ。ログ出力は行わない。"""
        return cls._err(message, loglevel=None, log_message_body=None)

    @classmethod
    def shield_exception[R, F: AnyError, **P](
        cls,
        *,
        loglevel: LogLevel = "error",
    ) -> Callable[[Callable[P, Result[R, F]]], Callable[P, Result[R, F | FatalError]]]:
        """関数内の例外を捕捉して FatalError を含む Result に変換するデコレータ"""

        def decorator(func: Callable[P, Result[R, F]]) -> Callable[P, Result[R, F | FatalError]]:
            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, F | FatalError]:
                try:
                    return cast(Result[R, F | FatalError], func(*args, **kwargs))
                except Exception as err:
                    exc: Any = err if loglevel == "error" else repr(err)
                    emit_log(loglevel, "Unhandled Exception Occurred!", exc=exc)
                    return cast(
                        Result[R, F | FatalError],
                        Result._err(
                            FatalError.from_exception(err),
                            loglevel=None,
                            log_message_body=None,
                        ),
                    )

            return wrapper

        return decorator

    @classmethod
    def error(
        cls,
        message: E | Result[T, E],
        log_message_body: str | None = None,
        **kwargs: Any,
    ) -> Result[T, E]:
        return cls._err(message, loglevel="error", log_message_body=log_message_body, **kwargs)

    @classmethod
    def warning(
        cls,
        message: E | Result[T, E],
        log_message_body: str | None = None,
        **kwargs: Any,
    ) -> Result[T, E]:
        return cls._err(message, loglevel="warning", log_message_body=log_message_body, **kwargs)

    @classmethod
    def info(
        cls,
        message: E | Result[T, E],
        log_message_body: str | None = None,
        **kwargs: Any,
    ) -> Result[T, E]:
        return cls._err(message, loglevel="info", log_message_body=log_message_body, **kwargs)

    @classmethod
    def debug(
        cls,
        message: E | Result[T, E],
        log_message_body: str | None = None,
        **kwargs: Any,
    ) -> Result[T, E]:
        return cls._err(message, loglevel="debug", log_message_body=log_message_body, **kwargs)

    def _type_name(self) -> str:
        return "Result"
