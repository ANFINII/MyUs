from django.db import transaction
from api.domain.follow import FilterOption, FollowDomain
from api.domain.user import UserDomain
from api.types.data.follow import FollowOutData, FollowUserData
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


def upsert_follow(follower: User, following: User) -> FollowOutData:
    follow = FollowDomain.get(follower, following)
    with transaction.atomic():
        if not follow:
            FollowDomain.create(follower, following)
        elif not follow.is_follow:
            FollowDomain.update(follow, is_follow=True)

        update_count(follower.id, following.id)


def delete_follow(follower: User, following: User) -> FollowOutData:
    follow = FollowDomain.get(follower, following)
    with transaction.atomic():
        FollowDomain.update(follow, is_follow=False)
        update_count(follower.id, following.id)


def update_count(follower_id: int, following_id: int) -> None:
    follower = UserDomain.get(id=follower_id)
    following = UserDomain.get(id=following_id)

    if follower:
        follower_count = follower.mypage.follower_count
        following_count = FollowDomain.count(FilterOption(follower_id=follower_id))
        UserDomain.update_count(follower, follower_count, following_count)

    if following:
        follower_count = FollowDomain.count(FilterOption(following_id=following_id))
        following_count = following.mypage.following_count
        UserDomain.update_count(following, follower_count, following_count)
