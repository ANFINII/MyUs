from api.src.domain.message import FilterOption, MessageDomain, SortOption
from api.src.types.data.message import MessageData, MessageReplyData
from api.utils.functions.user import get_author


def get_messages(chat_id: int) -> list[MessageData]:
    ids = MessageDomain.get_ids(FilterOption(chat_id=chat_id, is_parent=True), SortOption())
    objs = MessageDomain.bulk_get(ids)
    data = [
        MessageData(
            ulid=m.ulid,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=get_author(m.author),
        ) for m in objs
    ]
    return data


def get_replys(chat_id: int) -> list[MessageReplyData]:
    ids = MessageDomain.get_ids(FilterOption(chat_id=chat_id, is_parent=False), SortOption())
    objs = MessageDomain.bulk_get(ids)
    data = [
        MessageReplyData(
            ulid=m.ulid,
            parent_id=m.parent.ulid,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=get_author(m.author),
        ) for m in objs
    ]
    return data
