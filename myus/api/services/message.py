from api.domain.message import MessageDomain
from api.types.data.message import MessageData, MessageReplyData
from api.utils.functions.user import get_author


def get_messages(chat_id: int) -> list[MessageData]:
    objs = MessageDomain.get_messages(chat_id)
    data = [
        MessageData(
            id=m.id,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=get_author(m.author),
        ) for m in objs
    ]
    return data


def get_replys(chat_id: int) -> list[MessageReplyData]:
    objs = MessageDomain.get_replys(chat_id)
    data = [
        MessageReplyData(
            id=m.id,
            parent_id=m.parent.id,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=get_author(m.author),
        ) for m in objs
    ]
    return data
