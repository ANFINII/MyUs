from myus.utils.common.result import Result, ValidationError
from .data import VideoData
from ..common import MEDIA_TITLE_MAX


def validate(obj: VideoData) -> Result[None, ValidationError]:
    if len(obj.title) > MEDIA_TITLE_MAX:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.video) == 0:
        return Result.err(ValidationError("error.videoRequired"))

    return Result.ok(None)
