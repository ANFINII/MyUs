from django_ulid.models import ulid
from api.db.models.channel import Channel
from api.src.domain.interface.channel.data import ChannelData


def convert_data(obj: Channel) -> ChannelData:
    assert hasattr(obj, "subscribe_count"), "subscribe_count is required"
    return ChannelData(
        id=obj.id,
        ulid=obj.ulid,
        owner_id=obj.owner_id,
        owner_ulid=obj.owner.ulid,
        avatar=obj.avatar.name or "",
        name=obj.name,
        description=obj.description,
        is_default=obj.is_default,
        count=obj.subscribe_count,
    )


def marshal_data(data: ChannelData) -> Channel:
    return Channel(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        owner_id=data.owner_id,
        avatar=data.avatar,
        name=data.name,
        description=data.description,
        is_default=data.is_default,
    )
