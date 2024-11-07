from myus.api.models.user import User
from myus.api.models import Follow
from myus.api.types.dto.user import AuthorData, MediaUserData, NotificationUserData
from myus.api.utils.functions.index import create_url


def get_author(author: User) -> AuthorData:
    data = AuthorData(
        avatar=create_url(author.image()) or '',
        nickname=author.nickname,
        follower_count=author.mypage.follower_count,
    )
    return data


def get_media_user(user: User, obj) -> MediaUserData:
    data = MediaUserData(
        avatar=create_url(user.image()),
        nickname=user.nickname,
        is_like=obj.like.filter(id=user.id).exists(),
        is_follow=Follow.objects.filter(follower=user.id, following=obj.author).exists(),
    )
    return data


def get_notification_user(user: User) -> NotificationUserData:
    data = NotificationUserData(avatar=create_url(user.image()), nickname=user.nickname)
    return data
