from api.db.models.media import Chat
from api.src.domain.interface.media.chat.data import ChatData


def chat_data(obj: Chat) -> ChatData:
    return ChatData(
        id=obj.id,
        ulid=obj.ulid,
        channel_id=obj.channel_id,
        title=obj.title,
        content=obj.content,
        read=obj.read,
        period=obj.period,
        publish=obj.publish,
    )


def marshal_chat(data: ChatData) -> Chat:
    return Chat(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid,
        channel_id=data.channel_id,
        title=data.title,
        content=data.content,
        read=data.read,
        period=data.period,
        publish=data.publish,
    )
