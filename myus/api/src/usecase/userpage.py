from dataclasses import replace
from django.utils import timezone
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.domain.interface.advertise.interface import AdvertiseInterface
from api.src.domain.interface.follow.interface import FilterOption as FollowFilterOption, FollowInterface, SortOption as FollowSortOption
from api.src.domain.interface.media.index import ExcludeOption, FilterOption as MediaFilterOption, PageOption, SortOption as MediaSortOption
from api.src.injectors.container import injector
from api.src.types.dto.media import HomeDTO
from api.src.usecase.advertise import is_active
from api.src.usecase.media import get_videos, get_musics, get_blogs, get_comics, get_pictures, get_chats
from api.utils.common.result import FatalError, Result
from api.utils.functions.index import create_url


@Result.shield_exception()
def get_userpage_media(limit: int, search: str, owner_id: int, channel_id: int = 0) -> Result[HomeDTO, FatalError]:
    videos_ret = get_videos(search, owner_id=owner_id, channel_id=channel_id, limit=limit)
    if videos_ret.is_err:
        return Result.err(videos_ret.err_value)

    musics_ret = get_musics(search, owner_id=owner_id, channel_id=channel_id, limit=limit)
    if musics_ret.is_err:
        return Result.err(musics_ret.err_value)

    blogs_ret = get_blogs(search, owner_id=owner_id, channel_id=channel_id, limit=limit)
    if blogs_ret.is_err:
        return Result.err(blogs_ret.err_value)

    comics_ret = get_comics(search, owner_id=owner_id, channel_id=channel_id, limit=limit)
    if comics_ret.is_err:
        return Result.err(comics_ret.err_value)

    pictures_ret = get_pictures(search, owner_id=owner_id, channel_id=channel_id, limit=limit)
    if pictures_ret.is_err:
        return Result.err(pictures_ret.err_value)

    chats_ret = get_chats(search, owner_id=owner_id, channel_id=channel_id, limit=limit)
    if chats_ret.is_err:
        return Result.err(chats_ret.err_value)

    videos, _ = videos_ret.ok_value
    musics, _ = musics_ret.ok_value
    blogs, _ = blogs_ret.ok_value
    comics, _ = comics_ret.ok_value
    pictures, _ = pictures_ret.ok_value
    chats, _ = chats_ret.ok_value
    return Result.ok(HomeDTO(videos=videos, musics=musics, blogs=blogs, comics=comics, pictures=pictures, chats=chats))


@Result.shield_exception()
def get_userpage_advertises(search: str, owner_id: int) -> Result[list[AdvertiseData], FatalError]:
    repository = injector.get(AdvertiseInterface)
    ids_ret = repository.get_ids(MediaFilterOption(search=search, publish=True, owner_id=owner_id), ExcludeOption(), MediaSortOption(is_asc=True), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    today = timezone.localdate()
    return Result.ok([replace(o, image=create_url(o.image), video=create_url(o.video)) for o in objs if is_active(o, today)])


@Result.shield_exception()
def is_following(follower_id: int, following_id: int) -> Result[bool, FatalError]:
    follow_repo = injector.get(FollowInterface)
    ids_ret = follow_repo.get_ids(FollowFilterOption(follower_id=follower_id, following_id=following_id), FollowSortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.ok(False)

    follows_ret = follow_repo.bulk_get(ids)
    if follows_ret.is_err:
        return Result.err(follows_ret.err_value)

    follows = follows_ret.ok_value
    return Result.ok(follows[0].is_follow)
