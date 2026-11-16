from myus.utils.common.result import Result, ValidationError
from .data import SeriesData


SERIES_TITLE_MAX_LENGTH = 100
SERIES_MEDIA_MAX_COUNT = 200


def validate(obj: SeriesData) -> Result[None, ValidationError]:
    if len(obj.title) == 0 or len(obj.title) > SERIES_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.media_ids) > SERIES_MEDIA_MAX_COUNT or len(set(obj.media_ids)) != len(obj.media_ids):
        return Result.err(ValidationError("error.saveFailed"))

    return Result.ok(None)
