from django_ulid.models import ulid
from api.db.models.media import Chat
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.media.chat.data import ChatData


def convert_data(obj: Chat) -> ChatData:
    return ChatData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        read=obj.read,
        period=obj.period,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        like_count=obj.like.count(),
        thread_count=obj.thread_count(),
        joined_count=obj.joined_count(),
        channel=ChannelData(
            id=obj.channel.id,
            ulid=obj.channel.ulid,
            owner_id=obj.channel.owner_id,
            avatar=obj.channel.avatar.name if obj.channel.avatar else "",
            name=obj.channel.name,
            description=obj.channel.description,
            is_default=obj.channel.is_default,
            count=obj.channel.count,
        ),
    )


def marshal_data(data: ChatData) -> Chat:
    return Chat(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        channel_id=data.channel.id,
        title=data.title,
        content=data.content,
        read=data.read,
        period=data.period,
        publish=data.publish,
    )
