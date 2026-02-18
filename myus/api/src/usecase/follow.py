from dataclasses import replace
from django.db import transaction
from api.src.domain.entity.follow.repository import FollowRepository
from api.src.domain.entity.user.repository import UserRepository
from api.src.domain.interface.follow.data import FollowData
from api.src.domain.interface.follow.interface import FilterOption, SortOption
from api.src.domain.interface.user.data import UserAllData, UserData
from api.src.domain.interface.user.interface import FilterOption as UserFilterOption, SortOption as UserSortOption, UserInterface
from api.src.types.data.follow import FollowCreateData, FollowOutData, FollowUserData
from api.utils.functions.index import create_url


def get_follows(user_id: int, search: str | None, limit: int) -> list[FollowUserData]:
    follow_repo = FollowRepository()
    user_repo = UserRepository()

    ids = follow_repo.get_ids(FilterOption(follower_id=user_id, search=search or ""), SortOption(), limit)
    follows = follow_repo.bulk_get(ids)

    following_ids = [f.following_id for f in follows]
    users = user_repo.bulk_get(following_ids)
    user_map = {u.user.id: u for u in users}

    return [
        FollowUserData(
            avatar=create_url(user_map[f.following_id].user.avatar),
            nickname=user_map[f.following_id].user.nickname,
            introduction=user_map[f.following_id].profile.introduction,
            follower_count=user_map[f.following_id].mypage.follower_count,
            following_count=user_map[f.following_id].mypage.following_count,
        ) for f in follows if f.following_id in user_map
    ]


def get_followers(user_id: int, search: str | None, limit: int) -> list[FollowUserData]:
    follow_repo = FollowRepository()
    user_repo = UserRepository()

    ids = follow_repo.get_ids(FilterOption(following_id=user_id, search=search or ""), SortOption(), limit)
    follows = follow_repo.bulk_get(ids)

    follower_ids = [f.follower_id for f in follows]
    users = user_repo.bulk_get(follower_ids)
    user_map = {u.user.id: u for u in users}

    return [
        FollowUserData(
            avatar=create_url(user_map[f.follower_id].user.avatar),
            nickname=user_map[f.follower_id].user.nickname,
            introduction=user_map[f.follower_id].profile.introduction,
            follower_count=user_map[f.follower_id].mypage.follower_count,
            following_count=user_map[f.follower_id].mypage.following_count,
        ) for f in follows if f.follower_id in user_map
    ]


def upsert_follow(follower: UserAllData, ulid: str, is_follow: bool, repository: UserInterface) -> FollowOutData | None:
    follow_repo = FollowRepository()

    user_ids = repository.get_ids(UserFilterOption(ulid=ulid), UserSortOption())
    if len(user_ids) == 0:
        return None

    followings = repository.bulk_get(user_ids)
    if len(followings) == 0:
        return None

    following = followings[0]
    follow_ids = follow_repo.get_ids(FilterOption(follower_id=follower.user.id, following_id=following.user.id), SortOption())
    follow_data_list = follow_repo.bulk_get(follow_ids)
    follow = follow_data_list[0] if len(follow_data_list) > 0 else None
    follow_create = FollowCreateData(follower_id=follower.user.id, following_id=following.user.id, is_follow=is_follow)

    with transaction.atomic():
        if follow is None:
            follow_repo.bulk_save([FollowData(
                id=0,
                follower_id=follow_create.follower_id,
                following_id=follow_create.following_id,
                is_follow=follow_create.is_follow,
            )])
        else:
            updated_follow = replace(follow, is_follow=is_follow)
            follow_repo.bulk_save([updated_follow])

        follower_count = follow_repo.count(FilterOption(following_id=following.user.id))
        following_count = follow_repo.count(FilterOption(follower_id=follower.user.id))

        follower_mypage = replace(follower.mypage, following_count=following_count)
        updated_follower = replace(follower, mypage=follower_mypage)

        following_mypage = replace(following.mypage, follower_count=follower_count)
        updated_following = replace(following, mypage=following_mypage)

        repository.bulk_save([updated_follower, updated_following])

    return FollowOutData(is_follow=is_follow, follower_count=follower_count)
