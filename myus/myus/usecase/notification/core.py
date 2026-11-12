from myus.domain.notification.data import NotificationContentData
from myus.domain.notification.interface import FilterOption, NotificationInterface, SortOption
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, Result
from ._convert import get_notification_data, get_notification_user_map_data, get_user_enabled_types_data
from ..dto.notification import NotificationItemDTO, NotificationDTO


@Result.shield_exception()
def get_notification(user_id: int) -> Result[NotificationDTO, FatalError]:
    enabled_types_ret = get_user_enabled_types_data(user_id)
    if enabled_types_ret.is_err:
        return Result.err(enabled_types_ret.err_value)

    enabled_types = enabled_types_ret.ok_value
    if len(enabled_types) == 0:
        return Result.ok(NotificationDTO(count=0, items=[]))

    repo = injector.get(NotificationInterface)
    objs_ret = get_notification_data(user_id, enabled_types)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    confirmed_ids_ret = repo.get_ids(FilterOption(confirmed_user_id=user_id), SortOption())
    if confirmed_ids_ret.is_err:
        return Result.err(confirmed_ids_ret.err_value)

    confirmed_notification_ids = confirmed_ids_ret.ok_value
    confirmed_ids = set(confirmed_notification_ids)

    user_ids = list({n.user_from_id for n in objs} | {n.user_to_id for n in objs if n.user_to_id != 0})
    user_map_ret = get_notification_user_map_data(user_ids)
    if user_map_ret.is_err:
        return Result.err(user_map_ret.err_value)

    user_map = user_map_ret.ok_value

    items: list[NotificationItemDTO] = []
    for o in objs:
        user_from = user_map.get(o.user_from_id)
        if user_from is None or o.content is None:
            continue

        item = NotificationItemDTO(
            ulid=o.ulid,
            user_from=user_from,
            user_to=user_map.get(o.user_to_id),
            type_no=o.type_no,
            type_name=o.type_name,
            object_type=o.object_type,
            content_object=NotificationContentData(
                id=o.object_id,
                ulid=o.content.ulid,
                title=o.content.title,
                text=o.content.text,
                read=o.content.read,
                media_type=o.content.media_type,
                media_ulid=o.content.media_ulid,
                thread_ulid=o.content.thread_ulid,
            ),
            is_confirmed=o.id in confirmed_ids,
        )
        items.append(item)

    return Result.ok(NotificationDTO(count=len([item for item in items if not item.is_confirmed]), items=items))


@Result.shield_exception()
def notification_delete(user_id: int, ulid: str) -> Result[None, FatalError]:
    repo = injector.get(NotificationInterface)
    ret = repo.delete_by_user(ulid, user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def notification_confirm(user_id: int, ulid: str) -> Result[None, FatalError]:
    repo = injector.get(NotificationInterface)
    ret = repo.confirm(ulid, user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)
