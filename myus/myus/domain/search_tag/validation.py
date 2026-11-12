from myus.utils.common.result import Result, ValidationError
from .data import SearchTagData


SEARCH_TAG_MAX_COUNT = 20


def validate(objs: list[SearchTagData]) -> Result[None, ValidationError]:
    if len(objs) > SEARCH_TAG_MAX_COUNT:
        return Result.err(ValidationError("error.searchTagLimit"))

    return Result.ok(None)
