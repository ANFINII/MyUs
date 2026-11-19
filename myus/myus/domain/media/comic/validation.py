from myus.utils.common.result import Result, ValidationError
from .data import ComicData


COMIC_TITLE_MAX_LENGTH = 100


def validate(obj: ComicData) -> Result[None, ValidationError]:
    if len(obj.title) > COMIC_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.pages) == 0:
        return Result.err(ValidationError("error.pageRequired"))

    if not 0 <= obj.free_pages < len(obj.pages):
        return Result.err(ValidationError("error.freePagesRange"))

    return Result.ok(None)
