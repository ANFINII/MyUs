from api.src.domain.interface.follow.interface import FilterOption as FollowFilterOption, FollowInterface, SortOption as FollowSortOption
from api.src.injectors.container import injector
from api.src.types.dto.media import HomeDTO
from api.src.usecase.media import get_videos, get_musics, get_blogs, get_comics, get_pictures, get_chats
from api.utils.common.result import FatalError, Result


@Result.shield_exception()
def get_userpage_media(limit: int, search: str, channel_id: int = 0) -> Result[HomeDTO, FatalError]:
    videos_ret = get_videos(search, channel_id=channel_id, limit=limit)
    if videos_ret.is_err:
        return Result.err(videos_ret.err_value)

    musics_ret = get_musics(search, channel_id=channel_id, limit=limit)
    if musics_ret.is_err:
        return Result.err(musics_ret.err_value)

    blogs_ret = get_blogs(search, channel_id=channel_id, limit=limit)
    if blogs_ret.is_err:
        return Result.err(blogs_ret.err_value)

    comics_ret = get_comics(search, channel_id=channel_id, limit=limit)
    if comics_ret.is_err:
        return Result.err(comics_ret.err_value)

    pictures_ret = get_pictures(search, channel_id=channel_id, limit=limit)
    if pictures_ret.is_err:
        return Result.err(pictures_ret.err_value)

    chats_ret = get_chats(search, channel_id=channel_id, limit=limit)
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
def is_following(follower_id: int, following_id: int) -> Result[bool, FatalError]:
    follow_repo = injector.get(FollowInterface)
    ids_ret = follow_repo.get_ids(FollowFilterOption(follower_id=follower_id, following_id=following_id), FollowSortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    if len(ids_ret.ok_value) == 0:
        return Result.ok(False)

    follows_ret = follow_repo.bulk_get(ids_ret.ok_value)
    if follows_ret.is_err:
        return Result.err(follows_ret.err_value)

    return Result.ok(follows_ret.ok_value[0].is_follow)
