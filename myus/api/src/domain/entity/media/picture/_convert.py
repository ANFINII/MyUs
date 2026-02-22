from django_ulid.models import ulid
from api.db.models.media import Picture
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.media.data import HashtagData
from api.src.domain.interface.media.picture.data import PictureData


def convert_data(obj: Picture) -> PictureData:
    return PictureData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=obj.image.name if obj.image else "",
        read=obj.read,
        like=obj.like.count(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        comment_count=obj.comment_count(),
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
        hashtags=[HashtagData(jp_name=h.jp_name) for h in obj.hashtag.all()],
    )


def marshal_data(data: PictureData) -> Picture:
    return Picture(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        channel_id=data.channel.id,
        title=data.title,
        content=data.content,
        image=data.image,
        read=data.read,
        publish=data.publish,
    )
