from dataclasses import replace
from django.db import transaction
from api.db.models.users import Follow
from api.src.domain.follow import FilterOption, FollowDomain, SortOption
from api.src.domain.interface.user.data import UserData
from api.src.domain.interface.user.interface import FilterOption as UserFilterOption, SortOption as UserSortOption, UserInterface
from api.src.types.data.follow import FollowCreateData, FollowOutData, FollowUserData
from api.utils.functions.index import create_url


def get_follows(user_id: int, search: str | None, limit: int) -> list[FollowUserData]:
    ids = FollowDomain.get_ids(FilterOption(follower_id=user_id, search=search or ""), SortOption(), limit)
    objs = FollowDomain.bulk_get(ids)
    return [
        FollowUserData(
            avatar=create_url(obj.following.avatar.url),
            nickname=obj.following.nickname,
            introduction=obj.following.profile.introduction,
            follower_count=obj.following.mypage.follower_count,
            following_count=obj.following.mypage.following_count,
        ) for obj in objs
    ]


def get_followers(user_id: int, search: str | None, limit: int) -> list[FollowUserData]:
    ids = FollowDomain.get_ids(FilterOption(following_id=user_id, search=search or ""), SortOption(), limit)
    objs = FollowDomain.bulk_get(ids)
    return [
        FollowUserData(
            avatar=create_url(obj.follower.avatar.url),
            nickname=obj.follower.nickname,
            introduction=obj.follower.profile.introduction,
            follower_count=obj.follower.mypage.follower_count,
            following_count=obj.follower.mypage.following_count,
        ) for obj in objs
    ]


def upsert_follow(follower: UserData, ulid: str, is_follow: bool, repository: UserInterface) -> FollowOutData | None:
    user_ids = repository.get_ids(UserFilterOption(ulid=ulid), UserSortOption())
    if len(user_ids) == 0:
        return None

    followings = repository.bulk_get(user_ids)
    if len(followings) == 0:
        return None

    following = followings[0]
    follow_ids = FollowDomain.get_ids(FilterOption(follower_id=follower.id, following_id=following.id), SortOption())
    follow = FollowDomain.bulk_get(follow_ids)[0] if len(follow_ids) > 0 else None
    follow_data = FollowCreateData(follower_id=follower.id, following_id=following.id, is_follow=is_follow)

    with transaction.atomic():
        if follow is None:
            FollowDomain.bulk_save([Follow(
                follower_id=follow_data.follower_id,
                following_id=follow_data.following_id,
                is_follow=follow_data.is_follow,
            )])
        else:
            follow.is_follow = is_follow
            FollowDomain.bulk_save([follow])

        follower_count = FollowDomain.count(FilterOption(following_id=following.id))
        following_count = FollowDomain.count(FilterOption(follower_id=follower.id))

        follower_mypage = replace(follower.mypage, following_count=following_count)
        follower = replace(follower, mypage=follower_mypage)

        following_mypage = replace(following.mypage, follower_count=follower_count)
        following = replace(following, mypage=following_mypage)

        repository.bulk_save([follower, following])

    return FollowOutData(is_follow=is_follow, follower_count=follower_count)
