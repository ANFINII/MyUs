from .errors import AnyError, FatalError, NotFoundError, UnauthorizedError
from .result import Result
from .fatal import ResultFatal

__all__ = [
    "AnyError",
    "FatalError",
    "NotFoundError",
    "Result",
    "ResultFatal",
    "UnauthorizedError",
]
