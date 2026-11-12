from myus.domain.interface.media.comic.data import ComicData
from myus.utils.common.result import Result, ValidationError


COMIC_TITLE_MAX_LENGTH = 100


def validate(obj: ComicData) -> Result[None, ValidationError]:
    if len(obj.title) > COMIC_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.pages) == 0:
        return Result.err(ValidationError("error.pageRequired"))

    return Result.ok(None)
