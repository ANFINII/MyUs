from apps.myus.models.user import User
from apps.myus.models import Follow
from apps.api.types.user import Author, MediaUser, NotificationUser
from apps.api.utils.functions.index import create_url


def get_author(author: User) -> Author:
    data = Author(
        avatar=create_url(author.image()) or '',
        nickname=author.nickname,
        follower_count=author.mypage.follower_count,
    )
    return data


def get_media_user(user: User, obj) -> MediaUser:
    data = MediaUser(
        avatar=create_url(user.image()),
        nickname=user.nickname,
        is_like=obj.like.filter(id=user.id).exists(),
        is_follow=Follow.objects.filter(follower=user.id, following=obj.author).exists(),
    )
    return data


def get_notification_user(user: User) -> NotificationUser:
    data = NotificationUser(avatar=create_url(user.image()), nickname=user.nickname)
    return data
