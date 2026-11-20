from myus.utils.common.result import Result, ValidationError
from .data import AudioData, HiresData
from ..common import MEDIA_TITLE_MAX


HIRES_BIT_DEPTH = 24
HIRES_SAMPLE_RATE_MIN = 48000
HIRES_SAMPLE_RATE_MAX = 192000


def validate(obj: AudioData) -> Result[None, ValidationError]:
    if len(obj.title) > MEDIA_TITLE_MAX:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.audio) == 0:
        return Result.err(ValidationError("error.audioRequired"))

    if obj.hires is not None:
        return validate_hires(obj.hires)

    return Result.ok(None)


def validate_hires(obj: HiresData) -> Result[None, ValidationError]:
    if len(obj.file) == 0:
        return Result.err(ValidationError("error.fileRequired"))

    if obj.bit_depth != HIRES_BIT_DEPTH:
        return Result.err(ValidationError("error.hiresInvalid"))

    if not HIRES_SAMPLE_RATE_MIN <= obj.sample_rate <= HIRES_SAMPLE_RATE_MAX:
        return Result.err(ValidationError("error.hiresInvalid"))

    return Result.ok(None)
