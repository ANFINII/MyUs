from myus.domain.media.music.data import MusicData
from myus.utils.common.result import Result, ValidationError


MUSIC_TITLE_MAX_LENGTH = 100


def validate(obj: MusicData) -> Result[None, ValidationError]:
    if len(obj.title) > MUSIC_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.music) == 0:
        return Result.err(ValidationError("error.musicRequired"))

    return Result.ok(None)
