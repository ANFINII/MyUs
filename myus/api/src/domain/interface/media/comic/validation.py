from api.src.domain.interface.media.comic.data import ComicData
from api.utils.common.result import Result, ValidationError


COMIC_TITLE_MAX_LENGTH = 100


def validate_data(obj: ComicData) -> Result[None, ValidationError]:
    if len(obj.title) > COMIC_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))
    if len(obj.pages) == 0:
        return Result.err(ValidationError("error.comicPageRequired"))

    return Result.ok(None)


def validate_update_data(current: ComicData, update: ComicData) -> Result[None, ValidationError]:
    if current.pages != update.pages:
        return Result.err(ValidationError("error.comicPageNotChangeable"))

    return Result.ok(None)
