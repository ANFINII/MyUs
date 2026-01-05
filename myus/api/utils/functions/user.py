from api.db.models.user import User
from api.src.domain.follow import FollowDomain
from api.src.types.data.user import AuthorData, MediaUserData
from api.src.types.data.notification import NotificationUserData
from api.src.types.union.media import MediaModelType
from api.utils.functions.index import create_url


def get_author(author: User) -> AuthorData:
    data = AuthorData(
        avatar=create_url(author.image()) or "",
        ulid=author.ulid,
        nickname=author.nickname,
        follower_count=author.mypage.follower_count,
    )
    return data


def get_media_user(obj: MediaModelType, user: User | None) -> MediaUserData:
    follow = FollowDomain.get(user.id, obj.author.id) if user else None
    data = MediaUserData(
        is_like=obj.like.filter(id=user.id).exists() if user else False,
        is_follow=follow.is_follow if follow else False,
    )
    return data


def get_notification_user(user: User) -> NotificationUserData:
    data = NotificationUserData(avatar=create_url(user.image()), nickname=user.nickname)
    return data
