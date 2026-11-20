from myus.utils.common.result import Result, ValidationError
from .data import PictureData
from ..common import MEDIA_TITLE_MAX


def validate(obj: PictureData) -> Result[None, ValidationError]:
    if len(obj.title) > MEDIA_TITLE_MAX:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.image) == 0:
        return Result.err(ValidationError("error.imageRequired"))

    return Result.ok(None)
