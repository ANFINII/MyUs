from dataclasses import replace
from django.utils import timezone
from api.modules.logger import log
from api.src.domain.interface.media.chat.data import ChatData
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PAGE_SIZE, PageOption, SortOption
from api.src.domain.interface.message.interface import FilterOption as MessageFilterOption, MessageInterface, SortOption as MessageSortOption
from api.src.injectors.container import injector
from api.src.types.schema.media.input import ChatUpdateIn
from api.src.usecase.category import get_category_data
from api.src.usecase.notification import create_publish_notification
from api.src.usecase.manage.media._data import save_chat_data, delete_chat_data
from api.utils.common.result import FatalError, FindError, ForbiddenError, NotFoundError, Result, ValidationError, WriteError
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from api.utils.functions.transaction import atomic_result


@Result.shield_exception()
def get_manage_chats(user_id: int, search: str, channel_ulid: str = "", limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[ChatData], int], FatalError]:
    repo = injector.get(ChatInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    return Result.ok((objs, total))


@Result.shield_exception()
def get_manage_chat(user_id: int, ulid: str) -> Result[ChatData, FindError]:
    repo = injector.get(ChatInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    return Result.ok(objs[0])


@Result.shield_exception()
def update_manage_chat(user_id: int, ulid: str, input: ChatUpdateIn) -> Result[None, WriteError]:
    repo = injector.get(ChatInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Chat not found", ulid=ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    if obj.channel.owner_id != user_id:
        log.error("Chat owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    if timezone.localdate(input.publish_at) > input.period:
        return Result.err(ValidationError("error.publishAtAfterPeriod"))

    update_data = replace(obj, title=input.title, content=input.content, period=input.period, publish=input.publish, publish_at=input.publish_at)
    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value
    if category_data is None:
        return Result.err(ValidationError("error.categoryRequired"))

    save_ret = atomic_result(lambda: save_chat_data(update_data, category_data))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification(user_id, NotificationTypeNo.CHAT, obj.id, NotificationObjectType.CHAT)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_chat(user_id: int, ulids: list[str]) -> Result[None, FindError]:
    repo = injector.get(ChatInterface)
    ids_ret = repo.get_ids(FilterOption(ulids=ulids, owner_id=user_id), ExcludeOption(), SortOption(), PageOption(limit=len(ulids)))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    delete_ids = ids_ret.ok_value
    if len(delete_ids) != len(set(ulids)):
        log.error("Chat not found or owner mismatch", ulids=ulids, user_id=user_id)
        return Result.err(NotFoundError("error.deleteFailed"))

    message_repo = injector.get(MessageInterface)
    reply_ids: list[int] = []
    for chat_id in delete_ids:
        reply_ids_ret = message_repo.get_ids(MessageFilterOption(chat_id=chat_id, is_parent=False), MessageSortOption())
        if reply_ids_ret.is_err:
            return Result.err(reply_ids_ret.err_value)

        chat_reply_ids = reply_ids_ret.ok_value
        reply_ids += chat_reply_ids

    delete_ret = atomic_result(lambda: delete_chat_data(delete_ids, reply_ids))
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)
