from dataclasses import replace
from datetime import datetime
from myus.domain.media.audio.interface import AudioInterface
from myus.domain.playlist.data import PlaylistData
from myus.domain.playlist.interface import FilterOption, PlaylistInterface
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import AccessError, FatalError, FindError, NotFoundError, Result
from ._convert import audio_image, audio_urls, check_playlist_plan_data, get_audio_data, get_audio_ids_data, get_hidden_audio_ids_data, get_own_playlist_data, get_playlist_data, get_playlists_data, is_visible_audio, keep_hidden_audio_ids, playlist_image
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

    audio_repo = injector.get(AudioInterface)
    audios_ret = audio_repo.bulk_get(playlist.audio_ids)
    if audios_ret.is_err:
        return Result.err(audios_ret.err_value)

    all_audios = audios_ret.ok_value
    audios = [m for m in all_audios if is_visible_audio(m, user_id)]
    thumbnail_audio_ulids = [m.ulid for m in audios if playlist.image and audio_image(m) == playlist.image]
    return Result.ok(PlaylistDetailDTO(
        ulid=playlist.ulid,
        title=playlist.title,
        description=playlist.description,
        image=playlist_image(audios, playlist.image),
        thumbnail_audio_ulid=thumbnail_audio_ulids[0] if len(thumbnail_audio_ulids) > 0 else "",
        publish=playlist.publish,
        is_owner=is_owner,
        updated=playlist.updated,
        author=author,
        audios=audio_urls(audios),
    ))


@Result.shield_exception()
def create_playlist(user_id: int, input: PlaylistCreateDTO) -> Result[str, AccessError]:
    plan_ret = check_playlist_plan_data(user_id)
    if plan_ret.is_err:
        return Result.err(plan_ret.err_value)

    audio_ids: list[int] = []
    if len(input.audio_ulid) > 0:
        audio_ret = get_audio_data(input.audio_ulid, user_id)
        if audio_ret.is_err:
            return Result.err(audio_ret.err_value)

        audio = audio_ret.ok_value
        if audio is None:
            log.warning("not found", audio_ulid=input.audio_ulid)
            return Result.err(NotFoundError("error.createFailed"))

        audio_ids = [audio.id]

    repo = injector.get(PlaylistInterface)
    new_data = PlaylistData(id=0, ulid="", author_id=user_id, title=input.title, description="", image="", publish=input.publish, audio_ids=audio_ids, created=datetime.min, updated=datetime.min)
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
    plan_ret = check_playlist_plan_data(user_id)
    if plan_ret.is_err:
        return Result.err(plan_ret.err_value)

    playlist_ret = get_own_playlist_data(user_id, ulid, "error.saveFailed")
    if playlist_ret.is_err:
        return Result.err(playlist_ret.err_value)

    audio_ids_ret = get_audio_ids_data(input.audio_ulids, user_id)
    if audio_ids_ret.is_err:
        return Result.err(audio_ids_ret.err_value)

    playlist = playlist_ret.ok_value
    hidden_ids_ret = get_hidden_audio_ids_data(playlist.audio_ids, user_id)
    if hidden_ids_ret.is_err:
        return Result.err(hidden_ids_ret.err_value)

    thumbnail_ret = get_audio_data(input.thumbnail_audio_ulid, user_id) if input.thumbnail_audio_ulid else Result.ok(None)
    if thumbnail_ret.is_err:
        return Result.err(thumbnail_ret.err_value)

    audio_ids = audio_ids_ret.ok_value
    hidden_ids = hidden_ids_ret.ok_value
    thumbnail = thumbnail_ret.ok_value
    new_audio_ids = keep_hidden_audio_ids(playlist.audio_ids, audio_ids, hidden_ids)
    image = audio_image(thumbnail) if thumbnail is not None and thumbnail.id in audio_ids else ""
    repo = injector.get(PlaylistInterface)
    new_playlist = replace(playlist, title=input.title, description=input.description, image=image, publish=input.publish, audio_ids=new_audio_ids)
    save_ret = repo.bulk_save([new_playlist])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def add_playlist_audio(user_id: int, ulid: str, audio_ulid: str) -> Result[None, AccessError]:
    plan_ret = check_playlist_plan_data(user_id)
    if plan_ret.is_err:
        return Result.err(plan_ret.err_value)

    playlist_ret = get_own_playlist_data(user_id, ulid, "error.saveFailed")
    if playlist_ret.is_err:
        return Result.err(playlist_ret.err_value)

    audio_ret = get_audio_data(audio_ulid, user_id)
    if audio_ret.is_err:
        return Result.err(audio_ret.err_value)

    audio = audio_ret.ok_value
    if audio is None:
        log.warning("not found", audio_ulid=audio_ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    playlist = playlist_ret.ok_value
    if audio.id in playlist.audio_ids:
        return Result.ok(None)

    repo = injector.get(PlaylistInterface)
    save_ret = repo.bulk_save([replace(playlist, audio_ids=[*playlist.audio_ids, audio.id])])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def remove_playlist_audio(user_id: int, ulid: str, audio_ulid: str) -> Result[None, AccessError]:
    playlist_ret = get_own_playlist_data(user_id, ulid, "error.deleteFailed")
    if playlist_ret.is_err:
        return Result.err(playlist_ret.err_value)

    audio_ret = get_audio_data(audio_ulid, user_id)
    if audio_ret.is_err:
        return Result.err(audio_ret.err_value)

    audio = audio_ret.ok_value
    if audio is None:
        log.warning("not found", audio_ulid=audio_ulid)
        return Result.err(NotFoundError("error.deleteFailed"))

    playlist = playlist_ret.ok_value
    if audio.id not in playlist.audio_ids:
        return Result.ok(None)

    repo = injector.get(PlaylistInterface)
    save_ret = repo.bulk_save([replace(playlist, audio_ids=[audio_id for audio_id in playlist.audio_ids if audio_id != audio.id])])
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
