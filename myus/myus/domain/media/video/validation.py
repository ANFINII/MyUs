from myus.domain.media.video.data import VideoData
from myus.utils.common.result import Result, ValidationError


VIDEO_TITLE_MAX_LENGTH = 100


def validate(obj: VideoData) -> Result[None, ValidationError]:
    if len(obj.title) > VIDEO_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.video) == 0:
        return Result.err(ValidationError("error.videoRequired"))

    return Result.ok(None)
