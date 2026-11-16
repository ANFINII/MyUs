from dataclasses import replace
from datetime import datetime
from myus.domain.media.music.interface import MusicInterface
from myus.domain.playlist.data import PlaylistData
from myus.domain.playlist.interface import FilterOption, PlaylistInterface
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import AccessError, FatalError, FindError, NotFoundError, Result
from ._convert import get_music_data, get_music_ids_data, get_own_playlist_data, get_playlist_data, get_playlists_data, is_visible_music, music_urls
from ..dto.playlist import PlaylistCreateDTO, PlaylistDetailDTO, PlaylistDTO, PlaylistUpdateDTO
from ..user._convert import get_author_data
from ..user.core import get_user_data


@Result.shield_exception()
def get_my_playlists(user_id: int) -> Result[list[PlaylistDTO], FatalError]:
    return get_playlists_data(FilterOption(author_id=user_id), user_id)


@Result.shield_exception()
def get_user_playlists(user_ulid: str) -> Result[list[PlaylistDTO], FindError]:
    user_ret = get_user_data(ulid=user_ulid)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        log.info("not found", user_ulid=user_ulid)
        return Result.err(NotFoundError("error.userNotFound"))

    playlists_ret = get_playlists_data(FilterOption(author_id=user.user.id, publish=True), None)
    if playlists_ret.is_err:
        return Result.err(playlists_ret.err_value)

    playlists = playlists_ret.ok_value
    return Result.ok(playlists)


@Result.shield_exception()
def get_playlist(user_id: int | None, ulid: str) -> Result[PlaylistDetailDTO, FindError]:
    playlist_ret = get_playlist_data(ulid)
    if playlist_ret.is_err:
        return Result.err(playlist_ret.err_value)

    playlist = playlist_ret.ok_value
    is_owner = playlist is not None and playlist.author_id == user_id
    if playlist is None or (not is_owner and not playlist.publish):
        log.info("not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("error.playlistNotFound"))

    author_ret = get_author_data(playlist.author_id)
    if author_ret.is_err:
        return Result.err(author_ret.err_value)

    author = author_ret.ok_value

    music_repo = injector.get(MusicInterface)
    musics_ret = music_repo.bulk_get(playlist.music_ids)
    if musics_ret.is_err:
        return Result.err(musics_ret.err_value)

    all_musics = musics_ret.ok_value
    musics = [m for m in all_musics if is_visible_music(m, user_id)]
    return Result.ok(PlaylistDetailDTO(
        ulid=playlist.ulid,
        title=playlist.title,
        publish=playlist.publish,
        is_owner=is_owner,
        author=author,
        musics=music_urls(musics),
        updated=playlist.updated,
    ))


@Result.shield_exception()
def create_playlist(user_id: int, input: PlaylistCreateDTO) -> Result[str, FindError]:
    music_ids: list[int] = []
    if len(input.music_ulid) > 0:
        music_ret = get_music_data(input.music_ulid, user_id)
        if music_ret.is_err:
            return Result.err(music_ret.err_value)

        music = music_ret.ok_value
        if music is None:
            log.warning("not found", music_ulid=input.music_ulid)
            return Result.err(NotFoundError("error.createFailed"))

        music_ids = [music.id]

    repo = injector.get(PlaylistInterface)
    new_data = PlaylistData(id=0, ulid="", author_id=user_id, title=input.title, publish=input.publish, music_ids=music_ids, created=datetime.min, updated=datetime.min)
    save_ret = repo.bulk_save([new_data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    new_ids = save_ret.ok_value
    playlists_ret = repo.bulk_get(new_ids)
    if playlists_ret.is_err:
        return Result.err(playlists_ret.err_value)

    playlists = playlists_ret.ok_value
    assert len(playlists) == 1, "作成に失敗しました"
    return Result.ok(playlists[0].ulid)


@Result.shield_exception()
def update_playlist(user_id: int, ulid: str, input: PlaylistUpdateDTO) -> Result[None, AccessError]:
    playlist_ret = get_own_playlist_data(user_id, ulid, "error.saveFailed")
    if playlist_ret.is_err:
        return Result.err(playlist_ret.err_value)

    music_ids_ret = get_music_ids_data(input.music_ulids, user_id)
    if music_ids_ret.is_err:
        return Result.err(music_ids_ret.err_value)

    playlist = playlist_ret.ok_value
    music_ids = music_ids_ret.ok_value
    repo = injector.get(PlaylistInterface)
    save_ret = repo.bulk_save([replace(playlist, title=input.title, publish=input.publish, music_ids=music_ids)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def add_playlist_music(user_id: int, ulid: str, music_ulid: str) -> Result[None, AccessError]:
    playlist_ret = get_own_playlist_data(user_id, ulid, "error.saveFailed")
    if playlist_ret.is_err:
        return Result.err(playlist_ret.err_value)

    music_ret = get_music_data(music_ulid, user_id)
    if music_ret.is_err:
        return Result.err(music_ret.err_value)

    music = music_ret.ok_value
    if music is None:
        log.warning("not found", music_ulid=music_ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    playlist = playlist_ret.ok_value
    if music.id in playlist.music_ids:
        return Result.ok(None)

    repo = injector.get(PlaylistInterface)
    save_ret = repo.bulk_save([replace(playlist, music_ids=[*playlist.music_ids, music.id])])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def remove_playlist_music(user_id: int, ulid: str, music_ulid: str) -> Result[None, AccessError]:
    playlist_ret = get_own_playlist_data(user_id, ulid, "error.deleteFailed")
    if playlist_ret.is_err:
        return Result.err(playlist_ret.err_value)

    music_ret = get_music_data(music_ulid, user_id)
    if music_ret.is_err:
        return Result.err(music_ret.err_value)

    music = music_ret.ok_value
    if music is None:
        log.warning("not found", music_ulid=music_ulid)
        return Result.err(NotFoundError("error.deleteFailed"))

    playlist = playlist_ret.ok_value
    if music.id not in playlist.music_ids:
        return Result.ok(None)

    repo = injector.get(PlaylistInterface)
    save_ret = repo.bulk_save([replace(playlist, music_ids=[music_id for music_id in playlist.music_ids if music_id != music.id])])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_playlist(user_id: int, ulid: str) -> Result[None, AccessError]:
    playlist_ret = get_own_playlist_data(user_id, ulid, "error.deleteFailed")
    if playlist_ret.is_err:
        return Result.err(playlist_ret.err_value)

    playlist = playlist_ret.ok_value
    repo = injector.get(PlaylistInterface)
    delete_ret = repo.bulk_delete([playlist.id])
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)
