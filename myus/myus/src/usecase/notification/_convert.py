from myus.src.domain.interface.notification.data import NotificationData
from myus.src.domain.interface.notification.interface import FilterOption, NotificationInterface, SortOption
from myus.src.domain.interface.user.data import UserNotificationData
from myus.src.domain.interface.user.interface import UserInterface
from myus.src.injectors.container import injector
from myus.src.types.dto.notification import NotificationUserDTO
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.notification import NotificationObjectType, NotificationType, NotificationTypeNo
from myus.utils.functions.index import create_url


NOTIFICATION_LIMIT = 50


@Result.shield_exception()
def get_notification_data(receiver_id: int, enabled_types: tuple[NotificationTypeNo, ...]) -> Result[list[NotificationData], FatalError]:
    repo = injector.get(NotificationInterface)
    ids_ret = repo.get_ids(FilterOption(receiver_id=receiver_id, enabled_types=enabled_types, exclude_user_id=receiver_id), SortOption(), NOTIFICATION_LIMIT)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.ok([])

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    return Result.ok(objs)


@Result.shield_exception()
def get_notification_user_map_data(user_ids: list[int]) -> Result[dict[int, NotificationUserDTO], FatalError]:
    if len(user_ids) == 0:
        return Result.ok({})

    repo = injector.get(UserInterface)
    ret = repo.bulk_get(user_ids)
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


@Result.shield_exception()
def get_user_enabled_types_data(user_id: int) -> Result[tuple[NotificationTypeNo, ...], FatalError]:
    repo = injector.get(UserInterface)
    ret = repo.bulk_get([user_id])
    if ret.is_err:
        return Result.err(ret.err_value)

    users = ret.ok_value
    if len(users) == 0:
        return Result.ok(())

    return Result.ok(get_enabled_types(users[0].notification))


@Result.shield_exception()
def create_notification_data(user_from_id: int, user_to_id: int, type_no: NotificationTypeNo, object_id: int, object_type: NotificationObjectType) -> Result[None, FatalError]:
    if user_to_id != 0:
        if user_to_id == user_from_id and type_no != NotificationTypeNo.VIEWS:
            return Result.ok(None)
        enabled_types_ret = get_user_enabled_types_data(user_to_id)
        if enabled_types_ret.is_err:
            return Result.err(enabled_types_ret.err_value)

        enabled_types = enabled_types_ret.ok_value
        if type_no not in enabled_types:
            return Result.ok(None)

    repo = injector.get(NotificationInterface)
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
    save_ret = repo.bulk_save([notification])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def create_publish_notification_data(owner_id: int, type_no: NotificationTypeNo, object_id: int, object_type: NotificationObjectType) -> Result[None, FatalError]:
    repo = injector.get(NotificationInterface)
    ids_ret = repo.get_ids(FilterOption(type_no=type_no, object_type=object_type, object_ids=[object_id]), SortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) > 0:
        return Result.ok(None)

    create_ret = create_notification_data(owner_id, 0, type_no, object_id, object_type)
    if create_ret.is_err:
        return Result.err(create_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_notification_data(object_type: NotificationObjectType, object_ids: list[int], type_no: NotificationTypeNo | None = None, user_from_id: int = 0) -> Result[None, FatalError]:
    if len(object_ids) == 0:
        return Result.ok(None)

    repo = injector.get(NotificationInterface)
    ids_ret = repo.get_ids(FilterOption(type_no=type_no, object_type=object_type, object_ids=object_ids, user_from_id=user_from_id), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    delete_ret = repo.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)


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
