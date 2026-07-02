from __future__ import annotations

from typing import Any, Literal, assert_never

from api.modules.logger import log


type LogLevel = Literal["error", "warning", "info", "debug"]


def emit_log(loglevel: LogLevel, body: str, **kwargs: Any) -> None:
    """loglevel に応じて対応する log メソッドに委譲する。"""
    match loglevel:
        case "error":
            log.error(body, **kwargs)
        case "warning":
            log.warning(body, **kwargs)
        case "info":
            log.info(body, **kwargs)
        case "debug":
            log.debug(body, **kwargs)
        case _:
            assert_never(loglevel)
