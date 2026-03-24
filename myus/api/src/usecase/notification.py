from api.src.domain.interface.notification.data import NotificationData
from api.src.domain.interface.notification.interface import FilterOption, NotificationInterface, SortOption
from api.src.domain.interface.user.interface import UserInterface
from api.src.injectors.container import injector
from api.src.types.data.notification import NotificationContentData, NotificationItemData, NotificationOutData, NotificationUserData
from api.utils.functions.index import create_url


def get_notification_data(ulid: str = "", user_to_id: int = 0, exclude_user_id: int = 0) -> list[NotificationData]:
    repository = injector.get(NotificationInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, user_to_id=user_to_id, exclude_user_id=exclude_user_id), SortOption())
    if len(ids) == 0:
        return []

    return repository.bulk_get(ids)


def get_notification_user_map(user_ids: list[int]) -> dict[int, NotificationUserData]:
    if len(user_ids) == 0:
        return {}

    repository = injector.get(UserInterface)
    users = repository.bulk_get(user_ids)
    return {
        user.user.id: NotificationUserData(
            avatar=create_url(user.user.avatar),
            ulid=user.user.ulid,
            nickname=user.user.nickname,
        )
        for user in users
    }


def get_notification(user_id: int) -> NotificationOutData:
    repository = injector.get(NotificationInterface)
    objs = get_notification_data(user_to_id=user_id, exclude_user_id=user_id)
    confirmed_ids = set(repository.get_ids(FilterOption(confirmed_user_id=user_id), SortOption()))

    user_ids = list({n.user_from_id for n in objs} | {n.user_to_id for n in objs if n.user_to_id != 0})
    user_map = get_notification_user_map(user_ids)

    items: list[NotificationItemData] = []
    for o in objs:
        user_from = user_map.get(o.user_from_id)
        if user_from is None:
            continue

        item = NotificationItemData(
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

    return NotificationOutData(count=len(items), datas=items)


def notification_confirm(user_id: int, ulid: str) -> None:
    repository = injector.get(NotificationInterface)
    repository.confirm(ulid, user_id)


def notification_delete(user_id: int, ulid: str) -> None:
    repository = injector.get(NotificationInterface)
    repository.delete_by_user(ulid, user_id)
