from api.src.domain.interface.notification.data import NotificationData
from api.src.domain.interface.notification.interface import FilterOption, NotificationInterface, SortOption
from api.src.domain.interface.user.data import UserNotificationData
from api.src.domain.interface.user.interface import UserInterface
from api.src.injectors.container import injector
from api.src.types.dto.notification import NotificationContentData, NotificationItemDTO, NotificationDTO, NotificationUserDTO
from api.src.usecase.user import get_user_data
from api.utils.enum.notification import NotificationTypeNo
from api.utils.functions.index import create_url


def get_notification_data(receiver_id: int, enabled_types: tuple[NotificationTypeNo, ...]) -> list[NotificationData]:
    repository = injector.get(NotificationInterface)
    ids = repository.get_ids(FilterOption(receiver_id=receiver_id, enabled_types=enabled_types, exclude_user_id=receiver_id), SortOption())
    if len(ids) == 0:
        return []

    return repository.bulk_get(ids)


def get_notification_user_map(user_ids: list[int]) -> dict[int, NotificationUserDTO]:
    if len(user_ids) == 0:
        return {}

    repository = injector.get(UserInterface)
    users = repository.bulk_get(user_ids)
    return {
        user.user.id: NotificationUserDTO(
            avatar=create_url(user.user.avatar),
            ulid=user.user.ulid,
            nickname=user.user.nickname,
        )
        for user in users
    }


def get_enabled_types(setting: UserNotificationData) -> tuple[NotificationTypeNo, ...]:
    enabled = {
        NotificationTypeNo.VIDEO: setting.is_video,
        NotificationTypeNo.MUSIC: setting.is_music,
        NotificationTypeNo.BLOG: setting.is_blog,
        NotificationTypeNo.COMIC: setting.is_comic,
        NotificationTypeNo.PICTURE: setting.is_picture,
        NotificationTypeNo.CHAT: setting.is_chat,
        NotificationTypeNo.FOLLOW: setting.is_follow,
        NotificationTypeNo.LIKE: setting.is_like,
        NotificationTypeNo.REPLY: setting.is_reply,
        NotificationTypeNo.VIEWS: setting.is_views,
    }
    return tuple(type_no for type_no, is_enabled in enabled.items() if is_enabled)


def get_notification(user_id: int) -> NotificationDTO:
    user = get_user_data(user_id=user_id)
    enabled_types = get_enabled_types(user.notification) if user is not None else ()
    if len(enabled_types) == 0:
        return NotificationDTO(count=0, items=[])

    repository = injector.get(NotificationInterface)
    objs = get_notification_data(user_id, enabled_types)
    confirmed_ids = set(repository.get_ids(FilterOption(confirmed_user_id=user_id), SortOption()))

    user_ids = list({n.user_from_id for n in objs} | {n.user_to_id for n in objs if n.user_to_id != 0})
    user_map = get_notification_user_map(user_ids)

    items: list[NotificationItemDTO] = []
    for o in objs:
        user_from = user_map.get(o.user_from_id)
        if user_from is None:
            continue

        item = NotificationItemDTO(
            ulid=o.ulid,
            user_from=user_from,
            user_to=user_map.get(o.user_to_id),
            type_no=o.type_no,
            type_name=o.type_name,
            content_object=NotificationContentData(
                id=o.object_id,
                ulid=o.content.ulid,
                title=o.content.title,
                text=o.content.text,
                read=o.content.read,
            ),
            is_confirmed=o.id in confirmed_ids,
        )
        items.append(item)

    return NotificationDTO(count=len([item for item in items if not item.is_confirmed]), items=items)


def notification_confirm(user_id: int, ulid: str) -> None:
    repository = injector.get(NotificationInterface)
    repository.confirm(ulid, user_id)


def notification_delete(user_id: int, ulid: str) -> None:
    repository = injector.get(NotificationInterface)
    repository.delete_by_user(ulid, user_id)
