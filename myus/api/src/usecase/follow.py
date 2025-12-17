from dataclasses import asdict
from django.db import transaction
from api.models.user import User
from api.src.domain.follow import FilterOption, FollowDomain
from api.src.domain.user import UserDomain
from api.src.types.data.follow.index import FollowOutData, FollowUserData, FollowCreateData
from api.utils.functions.index import create_url


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
    follow = FollowDomain.get(follower.id, following.id)
    follow_data = FollowCreateData(follower_id=follower.id, following_id=following.id, is_follow=is_follow)
    with transaction.atomic():
        if not follow:
            FollowDomain.create(**asdict(follow_data))
        else:
            FollowDomain.update(follow, is_follow=is_follow)

        follower_count = FollowDomain.count(FilterOption(following_id=following.id))
        following_count = FollowDomain.count(FilterOption(follower_id=follower.id))
        UserDomain.update_mypage(follower, following_count=following_count)
        UserDomain.update_mypage(following, follower_count=follower_count)

    return FollowOutData(is_follow=is_follow, follower_count=follower_count)
