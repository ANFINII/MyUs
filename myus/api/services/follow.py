from api.domain.follow import FollowDomain
from api.types.data.follow import FollowUserData
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
