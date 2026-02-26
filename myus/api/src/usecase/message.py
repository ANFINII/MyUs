from dataclasses import replace
from datetime import datetime
from api.modules.logger import log
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption as MediaFilterOption, SortOption as MediaSortOption
from api.src.domain.interface.message.data import MessageData as MessageDomainData
from api.src.domain.interface.message.interface import FilterOption, MessageInterface, SortOption
from api.src.domain.interface.notification.data import NotificationData
from api.src.domain.interface.notification.interface import NotificationInterface
from api.src.injectors.container import injector
from api.src.types.data.message import MessageData, MessageReplyData
from api.src.usecase.user import get_author_data
from api.utils.enum.index import NotificationObjectType, NotificationType, NotificationTypeNo


def get_messages(chat_id: int) -> list[MessageData]:
    message_repo = injector.get(MessageInterface)
    ids = message_repo.get_ids(FilterOption(chat_id=chat_id, is_parent=True), SortOption(is_asc=True))
    messages = message_repo.bulk_get(ids)

    data = [
        MessageData(
            ulid=m.ulid,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=get_author_data(m.author_id),
        ) for m in messages
    ]
    return data


def get_replys(chat_id: int) -> list[MessageReplyData]:
    message_repo = injector.get(MessageInterface)
    ids = message_repo.get_ids(FilterOption(chat_id=chat_id, is_parent=False), SortOption(is_asc=True))
    messages = message_repo.bulk_get(ids)

    data = [
        MessageReplyData(
            ulid=m.ulid,
            parent_id=m.parent_ulid,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=get_author_data(m.author_id),
        ) for m in messages
    ]
    return data


def get_message_domain_data(message_ulid: str) -> MessageDomainData | None:
    message_repo = injector.get(MessageInterface)
    ids = message_repo.get_ids(FilterOption(message_ulid=message_ulid, is_parent=None), SortOption())
    if len(ids) == 0:
        log.warning("メッセージが見つかりませんでした", message_ulid=message_ulid)
        return None

    messages = message_repo.bulk_get(ids)
    return messages[0]


def create_message(user_id: int, chat_ulid: str, text: str, parent_ulid: str) -> MessageData | None:
    chat_repo = injector.get(ChatInterface)
    chat_ids = chat_repo.get_ids(MediaFilterOption(ulid=chat_ulid, publish=True), ExcludeOption(), MediaSortOption())
    if len(chat_ids) == 0:
        log.warning("チャットが見つかりませんでした", chat_ulid=chat_ulid)
        return None

    message_repo = injector.get(MessageInterface)

    parent_id: int | None = None
    if parent_ulid:
        parent_ids = message_repo.get_ids(FilterOption(message_ulid=parent_ulid, is_parent=True), SortOption())
        if len(parent_ids) == 0:
            log.warning("親メッセージが見つかりませんでした", parent_ulid=parent_ulid)
            return None
        parent_id = parent_ids[0]

    author = get_author_data(user_id)
    new_message = MessageDomainData(
        id=0,
        ulid="",
        author_id=user_id,
        chat_id=chat_ids[0],
        parent_id=parent_id,
        parent_ulid=parent_ulid,
        text=text,
        delta="",
        created=datetime.min,
        updated=datetime.min,
    )

    new_ids = message_repo.bulk_save([new_message])
    messages = message_repo.bulk_get(new_ids)
    assert len(messages) > 0, "メッセージの作成に失敗しました"
    message = messages[0]

    if parent_id is not None:
        parent_messages = message_repo.bulk_get([parent_id])
        if len(parent_messages) > 0 and parent_messages[0].author_id != user_id:
            notification_repo = injector.get(NotificationInterface)
            notification = NotificationData(
                id=0,
                user_from_id=user_id,
                user_to_id=parent_messages[0].author_id,
                type_no=NotificationTypeNo.REPLY,
                type_name=NotificationType.REPLY,
                object_id=message.id,
                object_type=NotificationObjectType.MESSAGE,
            )
            notification_repo.bulk_save([notification])

    data = MessageData(
        ulid=message.ulid,
        text=message.text,
        created=message.created,
        updated=message.updated,
        author=author,
    )
    return data


def get_replies(message_ulid: str) -> list[MessageReplyData]:
    message_repo = injector.get(MessageInterface)
    ids = message_repo.get_ids(FilterOption(parent_ulid=message_ulid, is_parent=False), SortOption(is_asc=True))
    messages = message_repo.bulk_get(ids)

    data = [
        MessageReplyData(
            ulid=m.ulid,
            parent_id=m.parent_ulid,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=get_author_data(m.author_id),
        ) for m in messages
    ]
    return data


def update_message(user_id: int, message_ulid: str, text: str) -> MessageData | None:
    message = get_message_domain_data(message_ulid)
    if message is None:
        return None

    if message.author_id != user_id:
        log.warning("メッセージの編集権限がありません", message_ulid=message_ulid, user_id=user_id)
        return None

    message_repo = injector.get(MessageInterface)
    updated_ids = message_repo.bulk_save([replace(message, text=text)])
    messages = message_repo.bulk_get(updated_ids)
    assert len(messages) == 1, "データが見つかりませんでした"
    updated = messages[0]

    data = MessageData(
        ulid=updated.ulid,
        text=updated.text,
        created=updated.created,
        updated=updated.updated,
        author=get_author_data(updated.author_id),
    )
    return data


def delete_message(user_id: int, message_ulid: str) -> str | None:
    message = get_message_domain_data(message_ulid)
    if message is None:
        return None

    if message.author_id != user_id:
        log.warning("メッセージの削除権限がありません", message_ulid=message_ulid, user_id=user_id)
        return None

    # 返信の場合はNotificationも削除
    if message.parent_id is not None:
        notification_repo = injector.get(NotificationInterface)
        notification_repo.delete(NotificationTypeNo.REPLY, message.id)

    chat_repo = injector.get(ChatInterface)
    chats = chat_repo.bulk_get([message.chat_id])
    if len(chats) == 0:
        log.warning("チャットが見つかりませんでした", chat_id=message.chat_id)
        return None

    message_repo = injector.get(MessageInterface)
    message_repo.delete(message.id)
    return chats[0].ulid
