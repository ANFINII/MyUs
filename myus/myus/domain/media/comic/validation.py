from myus.utils.common.result import Result, ValidationError
from .data import ComicData
from ..common import MEDIA_TITLE_MAX


def validate(obj: ComicData) -> Result[None, ValidationError]:
    if len(obj.title) > MEDIA_TITLE_MAX:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.pages) == 0:
        return Result.err(ValidationError("error.pageRequired"))

    if not 0 <= obj.free_pages < len(obj.pages):
        return Result.err(ValidationError("error.freePagesRange"))

    return Result.ok(None)
