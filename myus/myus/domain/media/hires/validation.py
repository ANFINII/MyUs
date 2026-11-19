from myus.utils.common.result import Result, ValidationError
from .data import MusicHiresData


HIRES_BIT_DEPTH = 24
HIRES_SAMPLE_RATE_MIN = 48000
HIRES_SAMPLE_RATE_MAX = 192000
HIRES_PRICE_MIN = 300
HIRES_PRICE_MAX = 600


def validate(obj: MusicHiresData) -> Result[None, ValidationError]:
    if obj.music_id == 0:
        return Result.err(ValidationError("error.musicRequired"))

    if len(obj.file) == 0:
        return Result.err(ValidationError("error.fileRequired"))

    if obj.bit_depth != HIRES_BIT_DEPTH:
        return Result.err(ValidationError("error.hiresInvalid"))

    if not HIRES_SAMPLE_RATE_MIN <= obj.sample_rate <= HIRES_SAMPLE_RATE_MAX:
        return Result.err(ValidationError("error.hiresInvalid"))

    if not HIRES_PRICE_MIN <= obj.price.amount <= HIRES_PRICE_MAX:
        return Result.err(ValidationError("error.priceRange"))

    return Result.ok(None)
