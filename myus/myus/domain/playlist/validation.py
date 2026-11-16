from myus.utils.common.result import Result, ValidationError
from .data import PlaylistData


PLAYLIST_TITLE_MAX_LENGTH = 100
PLAYLIST_MUSIC_MAX_COUNT = 200


def validate(obj: PlaylistData) -> Result[None, ValidationError]:
    if len(obj.title) == 0 or len(obj.title) > PLAYLIST_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.music_ids) > PLAYLIST_MUSIC_MAX_COUNT:
        return Result.err(ValidationError("error.playlistLimit"))

    return Result.ok(None)
