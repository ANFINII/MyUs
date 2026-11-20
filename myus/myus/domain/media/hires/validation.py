from myus.utils.common.result import Result, ValidationError
from .data import AudioHiresData


HIRES_BIT_DEPTH = 24
HIRES_SAMPLE_RATE_MIN = 48000
HIRES_SAMPLE_RATE_MAX = 192000


def validate(obj: AudioHiresData) -> Result[None, ValidationError]:
    if obj.audio_id == 0:
        return Result.err(ValidationError("error.audioRequired"))

    if len(obj.file) == 0:
        return Result.err(ValidationError("error.fileRequired"))

    if obj.bit_depth != HIRES_BIT_DEPTH:
        return Result.err(ValidationError("error.hiresInvalid"))

    if not HIRES_SAMPLE_RATE_MIN <= obj.sample_rate <= HIRES_SAMPLE_RATE_MAX:
        return Result.err(ValidationError("error.hiresInvalid"))

    return Result.ok(None)
