from django_ulid.models import ulid
from api.db.models.media import Chat
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.hashtag.data import HashtagData
from api.src.domain.interface.media.chat.data import ChatData


def convert_data(obj: Chat) -> ChatData:
    assert hasattr(obj, "like_count"), "like_count is required"
    assert hasattr(obj, "thread_total"), "thread_total is required"
    assert hasattr(obj, "joined_total"), "joined_total is required"
    category = next(iter(obj.category.all()), None)
    assert category is not None, "Category is required"
    return ChatData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        read=obj.read,
        like=obj.like_count,
        period=obj.period,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        thread_count=obj.thread_total,
        joined_count=obj.joined_total,
        category_ulid=category.ulid,
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
        hashtags=[HashtagData(id=t.id, ulid=t.ulid, name=t.name) for t in obj.hashtag.all()],
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
