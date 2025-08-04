from api.models.user import User
from api.models import Follow
from api.types.data.user import AuthorData, MediaUserData, NotificationUserData
from api.types.union.media import MediaModelType
from api.utils.functions.index import create_url
from api.domain.follow import FollowDomain


def get_author(author: User) -> AuthorData:
    data = AuthorData(
        avatar=create_url(author.image()) or "",
        ulid=author.ulid,
        nickname=author.nickname,
        follower_count=author.mypage.follower_count,
    )
    return data


def get_media_user(obj: MediaModelType, user: User | None) -> MediaUserData:
    data = MediaUserData(
        is_like=obj.like.filter(id=user.id).exists() if user else False,
        is_follow=FollowDomain.get(user, obj.author).is_follow if user else False,
    )
    return data


def get_notification_user(user: User) -> NotificationUserData:
    data = NotificationUserData(avatar=create_url(user.image()), nickname=user.nickname)
    return data
