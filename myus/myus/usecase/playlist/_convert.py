from dataclasses import replace
from django.utils import timezone
from myus.domain.media.audio.data import AudioData
from myus.domain.media.audio.interface import AudioInterface
from myus.domain.media.common import FilterOption as MediaFilterOption, PageOption as MediaPageOption, SortOption as MediaSortOption
from myus.domain.payment.plan import get_plan
from myus.domain.playlist.data import PlaylistData
from myus.domain.playlist.interface import FilterOption, PageOption, PlaylistInterface, SortOption
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import AccessError, FatalError, ForbiddenError, NotFoundError, Result
from myus.utils.functions.common import create_url
from ..dto.playlist import PlaylistDTO
from ..user.core import get_user_data


def is_visible_audio(audio: AudioData, user_id: int | None) -> bool:
    is_public = audio.publish and audio.publish_at <= timezone.now()
    return is_public or audio.channel.owner_id == user_id


def audio_image(audio: AudioData) -> str:
    return audio.image or audio.channel.avatar


def playlist_image(audios: list[AudioData], image: str) -> str:
    if image:
        return create_url(image)
    return create_url(audio_image(audios[0])) if len(audios) > 0 else ""


@Result.shield_exception()
def get_playlist_data(ulid: str) -> Result[PlaylistData | None, FatalError]:
    repo = injector.get(PlaylistInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid), SortOption(), PageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    playlists_ret = repo.bulk_get(ids)
    if playlists_ret.is_err:
        return Result.err(playlists_ret.err_value)

    playlists = playlists_ret.ok_value
    return Result.ok(playlists[0] if len(playlists) > 0 else None)


@Result.shield_exception()
def check_playlist_plan_data(user_id: int) -> Result[None, AccessError]:
    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    plan = get_plan(user.user_plan.plan) if user is not None else None
    if plan is None or not plan.is_playlist:
        log.info("plan required", user_id=user_id)
        return Result.err(ForbiddenError("error.playlistPlanRequired"))

    return Result.ok(None)


@Result.shield_exception()
def get_own_playlist_data(user_id: int, ulid: str, error: str) -> Result[PlaylistData, AccessError]:
    playlist_ret = get_playlist_data(ulid)
    if playlist_ret.is_err:
        return Result.err(playlist_ret.err_value)

    playlist = playlist_ret.ok_value
    if playlist is None:
        log.warning("not found", ulid=ulid)
        return Result.err(NotFoundError(error))

    if playlist.author_id != user_id:
        log.warning("author mismatch", ulid=ulid, user_id=user_id)
        return Result.err(ForbiddenError(error))

    return Result.ok(playlist)


@Result.shield_exception()
def get_playlists_data(filter: FilterOption, user_id: int | None) -> Result[list[PlaylistDTO], FatalError]:
    repo = injector.get(PlaylistInterface)
    ids_ret = repo.get_ids(filter, SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    playlists_ret = repo.bulk_get(ids)
    if playlists_ret.is_err:
        return Result.err(playlists_ret.err_value)

    playlists = playlists_ret.ok_value
    audio_repo = injector.get(AudioInterface)
    audios_ret = audio_repo.bulk_get(list({audio_id for p in playlists for audio_id in p.audio_ids}))
    if audios_ret.is_err:
        return Result.err(audios_ret.err_value)

    all_audios = audios_ret.ok_value
    audio_map = {m.id: m for m in all_audios if is_visible_audio(m, user_id)}
    data: list[PlaylistDTO] = []
    for p in playlists:
        audios = [audio_map[audio_id] for audio_id in p.audio_ids if audio_id in audio_map]
        image = playlist_image(audios, p.image)
        data.append(PlaylistDTO(ulid=p.ulid, title=p.title, image=image, publish=p.publish, count=len(audios), audio_ulids=[m.ulid for m in audios], updated=p.updated))

    return Result.ok(data)


@Result.shield_exception()
def get_audio_data(audio_ulid: str, user_id: int) -> Result[AudioData | None, FatalError]:
    repo = injector.get(AudioInterface)
    ids_ret = repo.get_ids(MediaFilterOption(ulid=audio_ulid), MediaSortOption(), MediaPageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    audios_ret = repo.bulk_get(ids)
    if audios_ret.is_err:
        return Result.err(audios_ret.err_value)

    all_audios = audios_ret.ok_value
    audios = [m for m in all_audios if is_visible_audio(m, user_id)]
    return Result.ok(audios[0] if len(audios) > 0 else None)


@Result.shield_exception()
def get_audio_ids_data(audio_ulids: list[str], user_id: int) -> Result[list[int], FatalError]:
    if len(audio_ulids) == 0:
        return Result.ok([])

    repo = injector.get(AudioInterface)
    ids_ret = repo.get_ids(MediaFilterOption(ulids=audio_ulids), MediaSortOption(), MediaPageOption(limit=0))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    audios_ret = repo.bulk_get(ids)
    if audios_ret.is_err:
        return Result.err(audios_ret.err_value)

    all_audios = audios_ret.ok_value
    ulid_map = {m.ulid: m.id for m in all_audios if is_visible_audio(m, user_id)}
    return Result.ok(list(dict.fromkeys(ulid_map[u] for u in audio_ulids if u in ulid_map)))


@Result.shield_exception()
def get_hidden_audio_ids_data(audio_ids: list[int], user_id: int) -> Result[set[int], FatalError]:
    repo = injector.get(AudioInterface)
    audios_ret = repo.bulk_get(audio_ids)
    if audios_ret.is_err:
        return Result.err(audios_ret.err_value)

    audios = audios_ret.ok_value
    return Result.ok({m.id for m in audios if not is_visible_audio(m, user_id)})


def keep_hidden_audio_ids(old_ids: list[int], new_ids: list[int], hidden_ids: set[int]) -> list[int]:
    ret = list(new_ids)
    for i, audio_id in enumerate(old_ids):
        if audio_id in hidden_ids:
            ret.insert(min(i, len(ret)), audio_id)
    return ret


def audio_urls(audios: list[AudioData]) -> list[AudioData]:
    return [replace(m, image=create_url(m.image), audio=create_url(m.audio)) for m in audios]
