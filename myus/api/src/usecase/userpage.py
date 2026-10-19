from api.src.domain.interface.follow.interface import FilterOption as FollowFilterOption, FollowInterface, SortOption as FollowSortOption
from api.src.injectors.container import injector
from api.src.types.dto.media import HomeDTO
from api.src.usecase.media import get_videos, get_musics, get_blogs, get_comics, get_pictures, get_chats
from api.utils.common.result import FatalError, Result


def get_userpage_media(limit: int, search: str, channel_id: int = 0) -> HomeDTO:
    videos, _ = get_videos(search, channel_id=channel_id, limit=limit)
    musics, _ = get_musics(search, channel_id=channel_id, limit=limit)
    blogs, _ = get_blogs(search, channel_id=channel_id, limit=limit)
    comics, _ = get_comics(search, channel_id=channel_id, limit=limit)
    pictures, _ = get_pictures(search, channel_id=channel_id, limit=limit)
    chats, _ = get_chats(search, channel_id=channel_id, limit=limit)
    return HomeDTO(videos=videos, musics=musics, blogs=blogs, comics=comics, pictures=pictures, chats=chats)


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
