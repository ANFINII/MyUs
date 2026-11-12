from collections.abc import Callable
from typing import Any, cast
from django.db import transaction
from ..common.result import AnyError, Result


class _RollbackError(Exception):
    def __init__(self, result: Result[Any, Any]) -> None:
        super().__init__()
        self.result = result


def atomic_result[T, E: AnyError](callback: Callable[[], Result[T, E]]) -> Result[T, E]:
    try:
        with transaction.atomic():
            ret = callback()
            if ret.is_err:
                raise _RollbackError(ret)
    except _RollbackError as rollback:
        return cast(Result[T, E], rollback.result)
    return ret
