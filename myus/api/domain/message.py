from api.models.message import Message
from api.types.data.message import MessageData, MessageReplyData
from api.utils.functions.user import get_author


class MessageDomain:
    @staticmethod
    def get_messages(chat_id: int) -> list[MessageData]:
        objs = Message.objects.filter(chat_id=chat_id, parent__isnull=True).select_related("author")
        return get_messages_data(objs)

    @staticmethod
    def get_replys(chat_id: int) -> list[MessageData]:
        objs = Message.objects.filter(chat_id=chat_id, parent__isnull=False).select_related("author")
        return get_replys_data(objs)


def get_messages_data(messages: list[Message]) -> list[MessageData]:
    data = [
        MessageData(
            id=m.id,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=get_author(m.author),
        ) for m in messages
    ]
    return data


def get_replys_data(messages: list[Message]) -> list[MessageReplyData]:
    data = [
        MessageReplyData(
            id=m.id,
            parent_id=m.parent.id,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=get_author(m.author),
        ) for m in messages
    ]
    return data
