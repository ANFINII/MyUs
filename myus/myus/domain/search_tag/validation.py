from myus.domain.search_tag.data import SearchTagData
from myus.utils.common.result import Result, ValidationError


SEARCH_TAG_MAX_COUNT = 20


def validate(objs: list[SearchTagData]) -> Result[None, ValidationError]:
    if len(objs) > SEARCH_TAG_MAX_COUNT:
        return Result.err(ValidationError("error.searchTagLimit"))

    return Result.ok(None)
