from django.core.mail import send_mail
from api.db.models.user import User
from api.src.domain.interface.subscribe.interface import FilterOption, SortOption, SubscribeInterface
from api.src.injectors.container import injector
from api.src.types.dto.notification import NotificationUserDTO
from api.src.types.dto.user import MediaUserDTO
from api.utils.functions.index import create_url


def get_media_user(is_like: bool, channel_id: int, user_id: int | None) -> MediaUserDTO:
    subscribe_repo = injector.get(SubscribeInterface)
    subscribe = None
    if user_id is not None:
        ids = subscribe_repo.get_ids(FilterOption(user_id=user_id, channel_id=channel_id), SortOption())
        subscribes = subscribe_repo.bulk_get(ids)
        subscribe = subscribes[0] if len(subscribes) > 0 else None

    data = MediaUserDTO(
        is_like=is_like,
        is_subscribe=subscribe.is_subscribe if subscribe else False,
    )

    return data


def get_notification_user(user: User) -> NotificationUserDTO:
    data = NotificationUserDTO(avatar=create_url(str(user.avatar)), ulid=user.ulid, nickname=user.nickname)
    return data


def email_user(user: User, subject: str, message: str, from_email: str | None = None, **kwargs) -> None:
    send_mail(subject, message, from_email, [user.email], **kwargs)
