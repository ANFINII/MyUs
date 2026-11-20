from myus.utils.common.result import Result, ValidationError
from .data import PlaylistData


PLAYLIST_TITLE_MAX_LENGTH = 100
PLAYLIST_DESCRIPTION_MAX_LENGTH = 1000
PLAYLIST_AUDIO_MAX_COUNT = 200


def validate(obj: PlaylistData) -> Result[None, ValidationError]:
    if len(obj.title) == 0 or len(obj.title) > PLAYLIST_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.description) > PLAYLIST_DESCRIPTION_MAX_LENGTH:
        return Result.err(ValidationError("error.descriptionLength"))

    if len(obj.audio_ids) > PLAYLIST_AUDIO_MAX_COUNT:
        return Result.err(ValidationError("error.playlistLimit"))

    return Result.ok(None)
