from api.db.models.message import Message
from api.src.domain.interface.message.data import MessageData


def message_data(obj: Message) -> MessageData:
    return MessageData(
        id=obj.id,
        ulid=obj.ulid,
        author_id=obj.author_id,
        chat_id=obj.chat_id,
        parent_id=obj.parent_id,
        text=obj.text,
        delta=obj.delta.html if obj.delta else "",
    )


def marshal_message(data: MessageData) -> Message:
    return Message(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid,
        author_id=data.author_id,
        chat_id=data.chat_id,
        parent_id=data.parent_id,
        text=data.text,
    )
