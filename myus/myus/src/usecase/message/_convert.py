from myus.modules.logger import log
from myus.src.domain.interface.message.data import MessageData
from myus.src.domain.interface.message.interface import FilterOption, MessageInterface, SortOption
from myus.src.injectors.container import injector
from myus.src.types.dto.message import MessageDTO
from myus.src.usecase.notification._convert import delete_notification_data
from myus.src.usecase.user._convert import get_author_map_data
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.notification import NotificationObjectType, NotificationTypeNo


@Result.shield_exception()
def get_message_data(message_ulid: str) -> Result[MessageData | None, FatalError]:
    repo = injector.get(MessageInterface)
    ids_ret = repo.get_ids(FilterOption(message_ulid=message_ulid, is_parent=None), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("メッセージが見つかりませんでした", message_ulid=message_ulid)
        return Result.ok(None)

    messages_ret = repo.bulk_get(ids)
    if messages_ret.is_err:
        return Result.err(messages_ret.err_value)

    messages = messages_ret.ok_value
    return Result.ok(messages[0])


@Result.shield_exception()
def save_message_data(data: MessageData) -> Result[None, FatalError]:
    repo = injector.get(MessageInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_message_data(data: MessageData, user_id: int) -> Result[None, FatalError]:
    # 返信の場合はNotificationも削除
    if data.parent_id is not None:
        notification_ret = delete_notification_data(NotificationObjectType.MESSAGE, [data.id], NotificationTypeNo.REPLY, user_id)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    repo = injector.get(MessageInterface)
    delete_ret = repo.bulk_delete([data.id])
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_messages_data(chat_id: int) -> Result[list[MessageDTO], FatalError]:
    repo = injector.get(MessageInterface)
    ids_ret = repo.get_ids(FilterOption(chat_id=chat_id, is_parent=True), SortOption(is_asc=True))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    messages_ret = repo.bulk_get(ids)
    if messages_ret.is_err:
        return Result.err(messages_ret.err_value)

    messages = messages_ret.ok_value
    author_map_ret = get_author_map_data(list({m.author_id for m in messages}))
    if author_map_ret.is_err:
        return Result.err(author_map_ret.err_value)

    author_map = author_map_ret.ok_value
    data = [
        MessageDTO(
            ulid=m.ulid,
            text=m.text,
            reply_count=m.reply_count,
            created=m.created,
            updated=m.updated,
            author=author_map[m.author_id],
        ) for m in messages
    ]

    return Result.ok(data)
