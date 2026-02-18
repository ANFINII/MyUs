from dataclasses import replace
from django.db import transaction
from api.src.domain.entity.follow.repository import FollowRepository
from api.src.domain.entity.user.repository import UserRepository
from api.src.domain.interface.follow.data import FollowData
from api.src.domain.interface.follow.interface import FilterOption, SortOption
from api.src.domain.interface.user.data import UserAllData, UserData
from api.src.domain.interface.user.interface import FilterOption as UserFilterOption, SortOption as UserSortOption, UserInterface
from api.src.types.data.follow import FollowOutData, FollowUserData
from api.utils.functions.index import create_url


def get_follows(user_id: int, search: str | None, limit: int) -> list[FollowUserData]:
    follow_repo = FollowRepository()
    user_repo = UserRepository()

    ids = follow_repo.get_ids(FilterOption(follower_id=user_id, search=search), SortOption(), limit)
    follows = follow_repo.bulk_get(ids)

    following_ids = [f.following_id for f in follows]
    users = user_repo.bulk_get(following_ids)

    return [
        FollowUserData(
            avatar=create_url(u.user.avatar),
            nickname=u.user.nickname,
            introduction=u.profile.introduction,
            follower_count=u.mypage.follower_count,
            following_count=u.mypage.following_count,
        ) for u in users
    ]


def get_followers(user_id: int, search: str | None, limit: int) -> list[FollowUserData]:
    follow_repo = FollowRepository()
    user_repo = UserRepository()

    ids = follow_repo.get_ids(FilterOption(following_id=user_id, search=search), SortOption(), limit)
    follows = follow_repo.bulk_get(ids)

    follower_ids = [f.follower_id for f in follows]
    users = user_repo.bulk_get(follower_ids)

    return [
        FollowUserData(
            avatar=create_url(u.user.avatar),
            nickname=u.user.nickname,
            introduction=u.profile.introduction,
            follower_count=u.mypage.follower_count,
            following_count=u.mypage.following_count,
        ) for u in users
    ]


def upsert_follow(follower: UserAllData, ulid: str, is_follow: bool, repository: UserInterface) -> FollowOutData | None:
    follow_repo = FollowRepository()

    user_ids = repository.get_ids(UserFilterOption(ulid=ulid), UserSortOption())
    if len(user_ids) == 0:
        return None

    following = repository.bulk_get(user_ids)[0]
    follower_id = follower.user.id
    following_id = following.user.id

    follow_ids = follow_repo.get_ids(FilterOption(follower_id=follower_id, following_id=following_id), SortOption())
    follow = follow_repo.bulk_get(follow_ids)[0]

    with transaction.atomic():
        if follow is None:
            follow_repo.bulk_save([FollowData(
                id=0,
                follower_id=follower_id,
                following_id=following_id,
                is_follow=is_follow,
            )])
        else:
            updated_follow = replace(follow, is_follow=is_follow)
            follow_repo.bulk_save([updated_follow])

        follower_count = follow_repo.count(FilterOption(following_id=following.user.id))
        following_count = follow_repo.count(FilterOption(follower_id=follower.user.id))

        follower_mypage = replace(follower.mypage, following_count=following_count)
        following_mypage = replace(following.mypage, follower_count=follower_count)

        updated_follower = replace(follower, mypage=follower_mypage)
        updated_following = replace(following, mypage=following_mypage)
        repository.bulk_save([updated_follower, updated_following])

    return FollowOutData(is_follow=is_follow, follower_count=follower_count)
