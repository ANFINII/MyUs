from myus.utils.common.result import Result, ValidationError
from .data import AudioData


AUDIO_TITLE_MAX_LENGTH = 100


def validate(obj: AudioData) -> Result[None, ValidationError]:
    if len(obj.title) > AUDIO_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.audio) == 0:
        return Result.err(ValidationError("error.audioRequired"))

    return Result.ok(None)
