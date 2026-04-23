from api.src.domain.interface.follow.interface import FilterOption as FollowFilterOption, FollowInterface, SortOption as FollowSortOption
from api.src.injectors.container import injector
from api.src.types.dto.media import HomeDTO
from api.src.usecase.media import get_videos, get_musics, get_blogs, get_comics, get_pictures, get_chats


def get_userpage_media(limit: int, search: str, channel_id: int = 0) -> HomeDTO:
    videos, _ = get_videos(search, channel_id=channel_id, limit=limit)
    musics, _ = get_musics(search, channel_id=channel_id, limit=limit)
    blogs, _ = get_blogs(search, channel_id=channel_id, limit=limit)
    comics, _ = get_comics(search, channel_id=channel_id, limit=limit)
    pictures, _ = get_pictures(search, channel_id=channel_id, limit=limit)
    chats, _ = get_chats(search, channel_id=channel_id, limit=limit)
    return HomeDTO(videos=videos, musics=musics, blogs=blogs, comics=comics, pictures=pictures, chats=chats)


def is_following(follower_id: int, following_id: int) -> bool:
    follow_repo = injector.get(FollowInterface)
    ids = follow_repo.get_ids(FollowFilterOption(follower_id=follower_id, following_id=following_id), FollowSortOption())
    if len(ids) == 0:
        return False

    follows = follow_repo.bulk_get(ids)
    return follows[0].is_follow
