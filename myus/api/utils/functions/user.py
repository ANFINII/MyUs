from django.core.mail import send_mail
from api.db.models.user import User
from api.src.domain.follow import FilterOption, FollowDomain, SortOption
from api.src.types.data.notification import NotificationUserData
from api.src.types.data.user import AuthorData, MediaUserData
from api.src.types.union.media import MediaModelType
from api.utils.functions.index import create_url


def get_author(author: User) -> AuthorData:
    data = AuthorData(
        avatar=create_url(str(author.avatar)) or "",
        ulid=author.ulid,
        nickname=author.nickname,
        follower_count=author.mypage.follower_count,
    )
    return data


def get_media_user(obj: MediaModelType, user_id: int | None) -> MediaUserData:
    follow = None
    if user_id is not None:
        ids = FollowDomain.get_ids(FilterOption(follower_id=user_id, following_id=obj.channel.owner.id), SortOption())
        follow = FollowDomain.bulk_get(ids)[0] if ids else None
    data = MediaUserData(
        is_like=obj.like.filter(id=user_id).exists() if user_id is not None else False,
        is_follow=follow.is_follow if follow else False,
    )
    return data


def get_notification_user(user: User) -> NotificationUserData:
    data = NotificationUserData(avatar=create_url(str(user.avatar)), nickname=user.nickname)
    return data


def email_user(user: User, subject: str, message: str, from_email: str | None = None, **kwargs) -> None:
    send_mail(subject, message, from_email, [user.email], **kwargs)
