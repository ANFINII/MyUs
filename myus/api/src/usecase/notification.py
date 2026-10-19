from api.src.domain.interface.notification.data import NotificationData
from api.src.domain.interface.notification.interface import FilterOption, NotificationInterface, SortOption
from api.src.domain.interface.user.data import UserNotificationData
from api.src.domain.interface.user.interface import UserInterface
from api.src.injectors.container import injector
from api.src.types.dto.notification import NotificationContentData, NotificationItemDTO, NotificationDTO, NotificationUserDTO
from api.utils.common.result import FatalError, Result
from api.utils.enum.notification import NotificationObjectType, NotificationType, NotificationTypeNo
from api.utils.functions.index import create_url


@Result.shield_exception()
def get_notification_data(receiver_id: int, enabled_types: tuple[NotificationTypeNo, ...]) -> Result[list[NotificationData], FatalError]:
    repository = injector.get(NotificationInterface)
    ids_ret = repository.get_ids(FilterOption(receiver_id=receiver_id, enabled_types=enabled_types, exclude_user_id=receiver_id), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.ok([])

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    return Result.ok(objs)


@Result.shield_exception()
def get_notification_user_map(user_ids: list[int]) -> Result[dict[int, NotificationUserDTO], FatalError]:
    if len(user_ids) == 0:
        return Result.ok({})

    repository = injector.get(UserInterface)
    ret = repository.bulk_get(user_ids)
    if ret.is_err:
        return Result.err(ret.err_value)

    users = ret.ok_value
    return Result.ok({
        user.user.id: NotificationUserDTO(
            avatar=create_url(user.user.avatar),
            ulid=user.user.ulid,
            nickname=user.user.nickname,
        )
        for user in users
    })


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


@Result.shield_exception()
def get_user_enabled_types(user_id: int) -> Result[tuple[NotificationTypeNo, ...], FatalError]:
    repository = injector.get(UserInterface)
    ret = repository.bulk_get([user_id])
    if ret.is_err:
        return Result.err(ret.err_value)

    users = ret.ok_value
    if len(users) == 0:
        return Result.ok(())

    return Result.ok(get_enabled_types(users[0].notification))


@Result.shield_exception()
def get_notification(user_id: int) -> Result[NotificationDTO, FatalError]:
    enabled_types_ret = get_user_enabled_types(user_id)
    if enabled_types_ret.is_err:
        return Result.err(enabled_types_ret.err_value)

    enabled_types = enabled_types_ret.ok_value
    if len(enabled_types) == 0:
        return Result.ok(NotificationDTO(count=0, items=[]))

    repository = injector.get(NotificationInterface)
    objs_ret = get_notification_data(user_id, enabled_types)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    confirmed_ids_ret = repository.get_ids(FilterOption(confirmed_user_id=user_id), SortOption())
    if confirmed_ids_ret.is_err:
        return Result.err(confirmed_ids_ret.err_value)

    confirmed_notification_ids = confirmed_ids_ret.ok_value
    confirmed_ids = set(confirmed_notification_ids)

    user_ids = list({n.user_from_id for n in objs} | {n.user_to_id for n in objs if n.user_to_id != 0})
    user_map_ret = get_notification_user_map(user_ids)
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
def create_notification(user_from_id: int, user_to_id: int, type_no: NotificationTypeNo, object_id: int, object_type: NotificationObjectType) -> Result[None, FatalError]:
    if user_to_id != 0:
        if user_to_id == user_from_id and type_no != NotificationTypeNo.VIEWS:
            return Result.ok(None)
        enabled_types_ret = get_user_enabled_types(user_to_id)
        if enabled_types_ret.is_err:
            return Result.err(enabled_types_ret.err_value)

        enabled_types = enabled_types_ret.ok_value
        if type_no not in enabled_types:
            return Result.ok(None)

    repository = injector.get(NotificationInterface)
    notification = NotificationData(
        id=0,
        ulid="",
        user_from_id=user_from_id,
        user_to_id=user_to_id,
        type_no=type_no,
        type_name=NotificationType[type_no.name],
        object_id=object_id,
        object_type=object_type,
        content=None,
    )
    save_ret = repository.bulk_save([notification])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def create_publish_notification(owner_id: int, type_no: NotificationTypeNo, object_id: int, object_type: NotificationObjectType) -> Result[None, FatalError]:
    repository = injector.get(NotificationInterface)
    ids_ret = repository.get_ids(FilterOption(type_no=type_no, object_type=object_type, object_ids=[object_id]), SortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) > 0:
        return Result.ok(None)

    create_ret = create_notification(owner_id, 0, type_no, object_id, object_type)
    if create_ret.is_err:
        return Result.err(create_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_object_notifications(object_type: NotificationObjectType, object_ids: list[int]) -> Result[None, FatalError]:
    if len(object_ids) == 0:
        return Result.ok(None)

    repository = injector.get(NotificationInterface)
    ids_ret = repository.get_ids(FilterOption(object_type=object_type, object_ids=object_ids), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    delete_ret = repository.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def notification_delete(user_id: int, ulid: str) -> Result[None, FatalError]:
    repository = injector.get(NotificationInterface)
    ret = repository.delete_by_user(ulid, user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def notification_confirm(user_id: int, ulid: str) -> Result[None, FatalError]:
    repository = injector.get(NotificationInterface)
    ret = repository.confirm(ulid, user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)
