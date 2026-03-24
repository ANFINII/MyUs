from api.src.domain.interface.notification.interface import FilterOption, NotificationInterface, SortOption
from api.src.domain.interface.user.interface import UserInterface
from api.src.injectors.container import injector
from api.src.types.data.notification import NotificationContentData, NotificationItemData, NotificationOutData, NotificationUserData
from api.utils.enum.index import NotificationTypeNo
from api.utils.functions.index import create_url


def get_notification(user_id: int) -> NotificationOutData:
    repository = injector.get(NotificationInterface)
    ids = repository.get_ids(FilterOption(user_to_id=user_id), SortOption())
    notifications = repository.bulk_get(ids)

    user_ids = list({n.user_from_id for n in notifications} | {n.user_to_id for n in notifications if n.user_to_id != 0})
    user_map = get_notification_user_map(user_ids)

    items: list[NotificationItemData] = []
    for n in notifications:
        user_from = user_map.get(n.user_from_id)
        if user_from is None:
            continue

        user_to = user_map.get(n.user_to_id)

        item = NotificationItemData(
            id=n.id,
            user_from=user_from,
            user_to=user_to,
            type_no=n.type_no,
            type_name=n.type_name,
            content_object=NotificationContentData(
                id=n.object_id,
                ulid=n.content.ulid,
                title=n.content.title,
                text=n.content.text,
                read=n.content.read,
            ),
            is_confirmed=False,
        )
        items.append(item)

    return NotificationOutData(count=len(items), datas=items)


def get_notification_user_map(user_ids: list[int]) -> dict[int, NotificationUserData]:
    if len(user_ids) == 0:
        return {}

    user_repo = injector.get(UserInterface)
    users = user_repo.bulk_get(user_ids)
    user_map: dict[int, NotificationUserData] = {}
    for user in users:
        user_map[user.user.id] = NotificationUserData(
            avatar=create_url(user.user.avatar),
            ulid=user.user.ulid,
            nickname=user.user.nickname,
        )
    return user_map


def delete_notification(type_no: NotificationTypeNo, object_id: int) -> None:
    repository = injector.get(NotificationInterface)
    repository.delete(type_no, object_id)
