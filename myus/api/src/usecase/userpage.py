from api.src.domain.interface.follow.interface import FilterOption as FollowFilterOption, FollowInterface, SortOption as FollowSortOption
from api.src.domain.interface.user.data import UserAllData
from api.src.domain.interface.user.interface import FilterOption as UserFilterOption, UserInterface
from api.src.injectors.container import injector
from api.src.types.data.media import HomeData
from api.src.usecase.media import get_videos, get_musics, get_comics, get_pictures, get_blogs, get_chats


def get_userpage_user(ulid: str) -> UserAllData | None:
    repository = injector.get(UserInterface)
    ids = repository.get_ids(UserFilterOption(ulid=ulid))
    if len(ids) == 0:
        return None

    users = repository.bulk_get(ids)
    user = users[0]
    if not user.user.is_active:
        return None

    return user


def get_userpage_media(limit: int, search: str, owner_id: int) -> HomeData:
    data = HomeData(
        videos=get_videos(limit, search, owner_id=owner_id),
        musics=get_musics(limit, search, owner_id=owner_id),
        comics=get_comics(limit, search, owner_id=owner_id),
        pictures=get_pictures(limit, search, owner_id=owner_id),
        blogs=get_blogs(limit, search, owner_id=owner_id),
        chats=get_chats(limit, search, owner_id=owner_id),
    )
    return data


def is_following(follower_id: int, following_id: int) -> bool:
    follow_repo = injector.get(FollowInterface)
    ids = follow_repo.get_ids(FollowFilterOption(follower_id=follower_id, following_id=following_id), FollowSortOption())
    if len(ids) == 0:
        return False

    follows = follow_repo.bulk_get(ids)
    return follows[0].is_follow
