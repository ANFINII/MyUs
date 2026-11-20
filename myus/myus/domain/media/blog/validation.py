from myus.utils.common.result import Result, ValidationError
from .data import BlogData
from ..common import MEDIA_TITLE_MAX


def validate(obj: BlogData) -> Result[None, ValidationError]:
    if len(obj.title) > MEDIA_TITLE_MAX:
        return Result.err(ValidationError("error.titleLength"))

    return Result.ok(None)
