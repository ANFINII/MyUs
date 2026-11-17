from dataclasses import replace
from django.utils import timezone
from myus.domain.media.common import FilterOption as MediaFilterOption, PageOption as MediaPageOption, SortOption as MediaSortOption
from myus.domain.media.music.data import MusicData
from myus.domain.media.music.interface import MusicInterface
from myus.domain.payment.plan import get_plan
from myus.domain.playlist.data import PlaylistData
from myus.domain.playlist.interface import FilterOption, PageOption, PlaylistInterface, SortOption
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import AccessError, FatalError, ForbiddenError, NotFoundError, Result
from myus.utils.functions.common import create_url
from ..dto.playlist import PlaylistDTO
from ..user.core import get_user_data


def is_visible_music(music: MusicData, user_id: int | None) -> bool:
    is_public = music.publish and music.publish_at <= timezone.now()
    return is_public or music.channel.owner_id == user_id


def get_thumbnail_music(musics: list[MusicData], thumbnail_music_id: int) -> MusicData | None:
    thumbnails = [m for m in musics if m.id == thumbnail_music_id]
    if len(thumbnails) > 0:
        return thumbnails[0]
    return musics[0] if len(musics) > 0 else None


def playlist_image(musics: list[MusicData], thumbnail_music_id: int) -> str:
    music = get_thumbnail_music(musics, thumbnail_music_id)
    if music is None:
        return ""
    return create_url(music.image or music.channel.avatar)


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
    music_repo = injector.get(MusicInterface)
    musics_ret = music_repo.bulk_get(list({music_id for p in playlists for music_id in p.music_ids}))
    if musics_ret.is_err:
        return Result.err(musics_ret.err_value)

    all_musics = musics_ret.ok_value
    music_map = {m.id: m for m in all_musics if is_visible_music(m, user_id)}
    data: list[PlaylistDTO] = []
    for p in playlists:
        musics = [music_map[music_id] for music_id in p.music_ids if music_id in music_map]
        image = playlist_image(musics, p.thumbnail_music_id)
        data.append(PlaylistDTO(ulid=p.ulid, title=p.title, publish=p.publish, count=len(musics), image=image, music_ulids=[m.ulid for m in musics], updated=p.updated))

    return Result.ok(data)


@Result.shield_exception()
def get_music_data(music_ulid: str, user_id: int) -> Result[MusicData | None, FatalError]:
    repo = injector.get(MusicInterface)
    ids_ret = repo.get_ids(MediaFilterOption(ulid=music_ulid), MediaSortOption(), MediaPageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    musics_ret = repo.bulk_get(ids)
    if musics_ret.is_err:
        return Result.err(musics_ret.err_value)

    all_musics = musics_ret.ok_value
    musics = [m for m in all_musics if is_visible_music(m, user_id)]
    return Result.ok(musics[0] if len(musics) > 0 else None)


@Result.shield_exception()
def get_music_ids_data(music_ulids: list[str], user_id: int) -> Result[list[int], FatalError]:
    if len(music_ulids) == 0:
        return Result.ok([])

    repo = injector.get(MusicInterface)
    ids_ret = repo.get_ids(MediaFilterOption(ulids=music_ulids), MediaSortOption(), MediaPageOption(limit=0))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    musics_ret = repo.bulk_get(ids)
    if musics_ret.is_err:
        return Result.err(musics_ret.err_value)

    all_musics = musics_ret.ok_value
    ulid_map = {m.ulid: m.id for m in all_musics if is_visible_music(m, user_id)}
    return Result.ok(list(dict.fromkeys(ulid_map[u] for u in music_ulids if u in ulid_map)))


@Result.shield_exception()
def get_hidden_music_ids_data(music_ids: list[int], user_id: int) -> Result[set[int], FatalError]:
    repo = injector.get(MusicInterface)
    musics_ret = repo.bulk_get(music_ids)
    if musics_ret.is_err:
        return Result.err(musics_ret.err_value)

    musics = musics_ret.ok_value
    return Result.ok({m.id for m in musics if not is_visible_music(m, user_id)})


def keep_hidden_music_ids(old_ids: list[int], new_ids: list[int], hidden_ids: set[int]) -> list[int]:
    ret = list(new_ids)
    for i, music_id in enumerate(old_ids):
        if music_id in hidden_ids:
            ret.insert(min(i, len(ret)), music_id)
    return ret


def music_urls(musics: list[MusicData]) -> list[MusicData]:
    return [replace(m, image=create_url(m.image), music=create_url(m.music)) for m in musics]
