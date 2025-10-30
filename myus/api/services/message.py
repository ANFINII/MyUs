from api.domain.message import MessageDomain
from api.types.data.message import MessageData, MessageReplyData
from api.utils.functions.user import get_author


def get_messages(chat_id: int) -> list[MessageData]:
    objs = MessageDomain.bulk_get(chat_id, is_parent=True)
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
    objs = MessageDomain.bulk_get(chat_id, is_parent=False)
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
