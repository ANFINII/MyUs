from api.domain.message import MessageDomain
from api.types.data.message import MessageData, MessageReplyData
from api.utils.functions.user import get_author


def get_messages(chat_id: int, is_parent: bool) -> list[MessageData]:
    objs = MessageDomain.bulk_get(chat_id, is_parent)
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
