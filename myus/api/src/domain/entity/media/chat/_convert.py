from django_ulid.models import ulid
from api.db.models.media import Chat
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.hashtag.data import HashtagData
from api.src.domain.interface.media.chat.data import ChatData


def convert_data(obj: Chat) -> ChatData:
    category = obj.category.first()
    assert category is not None, "Category is required"
    return ChatData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        read=obj.read,
        like=obj.like.count(),
        period=obj.period,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        thread_count=obj.thread_count(),
        joined_count=obj.joined_count(),
        channel=ChannelData(
            id=obj.channel.id,
            ulid=obj.channel.ulid,
            owner_id=obj.channel.owner_id,
            owner_ulid=obj.channel.owner.ulid,
            avatar=obj.channel.avatar.name if obj.channel.avatar else "",
            name=obj.channel.name,
            description=obj.channel.description,
            is_default=obj.channel.is_default,
            count=obj.channel.count,
        ),
        category_ulid=category.ulid,
        hashtags=[HashtagData(id=ch.hashtag.id, ulid=ch.hashtag.ulid, name=ch.hashtag.name) for ch in obj.chat_hashtags.all()],
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
