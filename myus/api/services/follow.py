from django.db import transaction
from api.domain.follow import FilterOption, FollowDomain
from api.domain.user import UserDomain
from api.types.data.follow.index import FollowOutData, FollowUserData
from api.utils.functions.index import create_url
from api.models.user import User


def get_follows(user_id: int, search: str | None, limit: int) -> list[FollowUserData]:
    objs = FollowDomain.get_follows(user_id, search, limit)
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
    objs = FollowDomain.get_followers(user_id, search, limit)
    return [
        FollowUserData(
            avatar=create_url(obj.follower.avatar.url),
            nickname=obj.follower.nickname,
            introduction=obj.follower.profile.introduction,
            follower_count=obj.follower.mypage.follower_count,
            following_count=obj.follower.mypage.following_count,
        ) for obj in objs
    ]


def upsert_follow(follower: User, following: User, is_follow: bool) -> FollowOutData:
    follow = FollowDomain.get(follower, following)
    with transaction.atomic():
        if not follow:
            FollowDomain.create(follower, following)
        else:
            FollowDomain.update(follow, is_follow=is_follow)

        follower_count = FollowDomain.count(FilterOption(following_id=following.id))
        following_count = FollowDomain.count(FilterOption(follower_id=follower.id))
        UserDomain.update_mypage(follower, following_count=following_count)
        UserDomain.update_mypage(following, follower_count=follower_count)

    return FollowOutData(is_follow=is_follow, follower_count=follower_count)
