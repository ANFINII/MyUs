from api.db.models.users import Follow
from api.src.domain.interface.follow.data import FollowData


def convert_data(obj: Follow) -> FollowData:
    return FollowData(
        id=obj.id,
        follower_id=obj.follower_id,
        following_id=obj.following_id,
        is_follow=obj.is_follow,
    )


def marshal_follow(data: FollowData) -> Follow:
    return Follow(
        id=data.id if data.id != 0 else None,
        follower_id=data.follower_id,
        following_id=data.following_id,
        is_follow=data.is_follow,
    )
