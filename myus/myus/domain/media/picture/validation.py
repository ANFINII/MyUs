from myus.domain.media.picture.data import PictureData
from myus.utils.common.result import Result, ValidationError


PICTURE_TITLE_MAX_LENGTH = 100


def validate(obj: PictureData) -> Result[None, ValidationError]:
    if len(obj.title) > PICTURE_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.image) == 0:
        return Result.err(ValidationError("error.imageRequired"))

    return Result.ok(None)
