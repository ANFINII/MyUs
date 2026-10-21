from dataclasses import replace
from datetime import datetime
from django.db import transaction
from api.modules.logger import log
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption as MediaFilterOption, PageOption, SortOption as MediaSortOption
from api.src.domain.interface.message.data import MessageData as MessageDomainData
from api.src.domain.interface.message.interface import FilterOption, MessageInterface, SortOption
from api.src.domain.interface.notification.interface import NotificationInterface
from api.src.injectors.container import injector
from api.src.types.dto.message import MessageDTO, MessageReplyDTO
from api.src.usecase.notification import create_notification
from api.src.usecase.user import get_author_data, get_author_data_map
from api.utils.common.result import AccessError, FatalError, FindError, ForbiddenError, NotFoundError, Result
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo


@Result.shield_exception()
def get_message_data(message_ulid: str) -> Result[MessageDomainData | None, FatalError]:
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
def save_message_data(data: MessageDomainData) -> Result[None, FatalError]:
    repo = injector.get(MessageInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_messages(chat_id: int) -> Result[list[MessageDTO], FatalError]:
    repo = injector.get(MessageInterface)
    ids_ret = repo.get_ids(FilterOption(chat_id=chat_id, is_parent=True), SortOption(is_asc=True))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    messages_ret = repo.bulk_get(ids)
    if messages_ret.is_err:
        return Result.err(messages_ret.err_value)

    messages = messages_ret.ok_value
    author_map_ret = get_author_data_map(list({m.author_id for m in messages}))
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


@Result.shield_exception()
def get_replies(message_ulid: str) -> Result[list[MessageReplyDTO], FatalError]:
    repo = injector.get(MessageInterface)
    ids_ret = repo.get_ids(FilterOption(parent_ulid=message_ulid, is_parent=False), SortOption(is_asc=True))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    messages_ret = repo.bulk_get(ids)
    if messages_ret.is_err:
        return Result.err(messages_ret.err_value)

    messages = messages_ret.ok_value
    author_map_ret = get_author_data_map(list({m.author_id for m in messages}))
    if author_map_ret.is_err:
        return Result.err(author_map_ret.err_value)

    author_map = author_map_ret.ok_value
    data = [
        MessageReplyDTO(
            ulid=m.ulid,
            parent_id=m.parent_ulid,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=author_map[m.author_id],
        ) for m in messages
    ]

    return Result.ok(data)


@Result.shield_exception()
def create_message(user_id: int, chat_ulid: str, text: str, parent_ulid: str) -> Result[MessageDTO, FindError]:
    chat_repo = injector.get(ChatInterface)
    chat_ids_ret = chat_repo.get_ids(MediaFilterOption(ulid=chat_ulid, publish=True), ExcludeOption(), MediaSortOption(), PageOption())
    if chat_ids_ret.is_err:
        return Result.err(chat_ids_ret.err_value)

    chat_ids = chat_ids_ret.ok_value
    if len(chat_ids) == 0:
        log.warning("チャットが見つかりませんでした", chat_ulid=chat_ulid)
        return Result.err(NotFoundError("error.messageCreateFailed"))

    repo = injector.get(MessageInterface)

    parent_id: int | None = None
    if parent_ulid:
        parent_ids_ret = repo.get_ids(FilterOption(chat_id=chat_ids[0], message_ulid=parent_ulid, is_parent=True), SortOption())
        if parent_ids_ret.is_err:
            return Result.err(parent_ids_ret.err_value)

        parent_ids = parent_ids_ret.ok_value
        if len(parent_ids) == 0:
            log.warning("親メッセージが見つかりませんでした", parent_ulid=parent_ulid)
            return Result.err(NotFoundError("error.messageCreateFailed"))
        parent_id = parent_ids[0]

    author_ret = get_author_data(user_id)
    if author_ret.is_err:
        return Result.err(author_ret.err_value)

    author = author_ret.ok_value
    new_message = MessageDomainData(
        id=0,
        ulid="",
        author_id=user_id,
        chat_id=chat_ids[0],
        parent_id=parent_id,
        parent_ulid=parent_ulid,
        text=text,
        reply_count=0,
        created=datetime.min,
        updated=datetime.min,
    )

    new_ids_ret = repo.bulk_save([new_message])
    if new_ids_ret.is_err:
        return Result.err(new_ids_ret.err_value)

    new_ids = new_ids_ret.ok_value
    messages_ret = repo.bulk_get(new_ids)
    if messages_ret.is_err:
        return Result.err(messages_ret.err_value)

    messages = messages_ret.ok_value
    assert len(messages) > 0, "error.messageCreateFailed"
    message = messages[0]

    if parent_id is not None:
        parent_messages_ret = repo.bulk_get([parent_id])
        if parent_messages_ret.is_err:
            return Result.err(parent_messages_ret.err_value)

        parent_messages = parent_messages_ret.ok_value
        if len(parent_messages) > 0:
            notification_ret = create_notification(user_id, parent_messages[0].author_id, NotificationTypeNo.REPLY, message.id, NotificationObjectType.MESSAGE)
            if notification_ret.is_err:
                log.error("通知の作成に失敗しました", error=notification_ret.err_value.message, message_id=message.id)

    data = MessageDTO(
        ulid=message.ulid,
        text=message.text,
        reply_count=0,
        created=message.created,
        updated=message.updated,
        author=author,
    )
    return Result.ok(data)


@Result.shield_exception()
def update_message(user_id: int, message_ulid: str, text: str) -> Result[str, AccessError]:
    message_ret = get_message_data(message_ulid)
    if message_ret.is_err:
        return Result.err(message_ret.err_value)

    message = message_ret.ok_value
    if message is None:
        return Result.err(NotFoundError("Not Found"))

    if message.author_id != user_id:
        log.warning("メッセージの編集権限がありません", message_ulid=message_ulid, user_id=user_id)
        return Result.err(ForbiddenError("Forbidden"))

    chat_repo = injector.get(ChatInterface)
    chats_ret = chat_repo.bulk_get([message.chat_id])
    if chats_ret.is_err:
        return Result.err(chats_ret.err_value)

    chats = chats_ret.ok_value
    if len(chats) == 0:
        log.warning("チャットが見つかりませんでした", chat_id=message.chat_id)
        return Result.err(NotFoundError("Not Found"))

    save_ret = save_message_data(replace(message, text=text))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(chats[0].ulid)


@Result.shield_exception()
def delete_message(user_id: int, message_ulid: str) -> Result[str, AccessError]:
    message_ret = get_message_data(message_ulid)
    if message_ret.is_err:
        return Result.err(message_ret.err_value)

    message = message_ret.ok_value
    if message is None:
        return Result.err(NotFoundError("Not Found"))

    if message.author_id != user_id:
        log.warning("メッセージの削除権限がありません", message_ulid=message_ulid, user_id=user_id)
        return Result.err(ForbiddenError("Forbidden"))

    chat_repo = injector.get(ChatInterface)
    chats_ret = chat_repo.bulk_get([message.chat_id])
    if chats_ret.is_err:
        return Result.err(chats_ret.err_value)

    chats = chats_ret.ok_value
    if len(chats) == 0:
        log.warning("チャットが見つかりませんでした", chat_id=message.chat_id)
        return Result.err(NotFoundError("Not Found"))

    with transaction.atomic():
        # 返信の場合はNotificationも削除
        if message.parent_id is not None:
            notification_repo = injector.get(NotificationInterface)
            notification_ret = notification_repo.delete(NotificationTypeNo.REPLY, NotificationObjectType.MESSAGE, message.id, user_id)
            if notification_ret.is_err:
                transaction.set_rollback(True)
                return Result.err(notification_ret.err_value)

        repo = injector.get(MessageInterface)
        delete_ret = repo.bulk_delete([message.id])
        if delete_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(delete_ret.err_value)

    return Result.ok(chats[0].ulid)
