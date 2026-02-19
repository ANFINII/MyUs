from django.core.mail import send_mail
from api.db.models.user import User
from api.src.domain.entity.subscribe.repository import SubscribeRepository
from api.src.domain.interface.subscribe.interface import FilterOption, SortOption
from api.src.types.data.notification import NotificationUserData
from api.src.types.data.user import MediaUserData
from api.src.types.union.media import MediaModelType
from api.utils.functions.index import create_url


def get_media_user(obj: MediaModelType, user_id: int | None) -> MediaUserData:
    repository = SubscribeRepository()
    subscribe = None
    if user_id is not None:
        ids = repository.get_ids(FilterOption(user_id=user_id, channel_id=obj.channel.id), SortOption())
        subscribes = repository.bulk_get(ids)
        subscribe = subscribes[0] if len(subscribes) > 0 else None
    data = MediaUserData(
        is_like=obj.like.filter(id=user_id).exists() if user_id is not None else False,
        is_subscribe=subscribe.is_subscribe if subscribe else False,
    )
    return data


def get_notification_user(user: User) -> NotificationUserData:
    data = NotificationUserData(avatar=create_url(str(user.avatar)), nickname=user.nickname)
    return data


def email_user(user: User, subject: str, message: str, from_email: str | None = None, **kwargs) -> None:
    send_mail(subject, message, from_email, [user.email], **kwargs)
