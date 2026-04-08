from api.src.domain.interface.follow.interface import FilterOption as FollowFilterOption, FollowInterface, SortOption as FollowSortOption
from api.src.injectors.container import injector
from api.src.types.dto.media import HomeDTO
from api.src.usecase.media import get_videos, get_musics, get_comics, get_pictures, get_blogs, get_chats


def get_userpage_media(limit: int, search: str, channel_id: int = 0) -> HomeDTO:
    data = HomeDTO(
        videos=get_videos(limit, search, channel_id=channel_id),
        musics=get_musics(limit, search, channel_id=channel_id),
        comics=get_comics(limit, search, channel_id=channel_id),
        pictures=get_pictures(limit, search, channel_id=channel_id),
        blogs=get_blogs(limit, search, channel_id=channel_id),
        chats=get_chats(limit, search, channel_id=channel_id),
    )
    return data


def is_following(follower_id: int, following_id: int) -> bool:
    follow_repo = injector.get(FollowInterface)
    ids = follow_repo.get_ids(FollowFilterOption(follower_id=follower_id, following_id=following_id), FollowSortOption())
    if len(ids) == 0:
        return False

    follows = follow_repo.bulk_get(ids)
    return follows[0].is_follow
