from django_ulid.models import ulid
from myus.db.models.media import Audio
from myus.domain.channel.data import ChannelData
from myus.domain.hashtag.data import HashtagData
from myus.domain.media.audio.data import AudioData


def convert_data(obj: Audio) -> AudioData:
    assert hasattr(obj, "like_count"), "like_count is required"
    category = next(iter(obj.category.all()), None)
    return AudioData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        lyric=obj.lyric,
        image=obj.image.name or "",
        audio=obj.audio.name or "",
        gain=obj.gain,
        read=obj.read,
        like=obj.like_count,
        publish=obj.publish,
        publish_at=obj.publish_at,
        created=obj.created,
        updated=obj.updated,
        category_ulid=category.ulid if category is not None else "",
        channel=ChannelData(
            id=obj.channel.id,
            ulid=obj.channel.ulid,
            owner_id=obj.channel.owner_id,
            owner_ulid=obj.channel.owner.ulid,
            avatar=obj.channel.avatar.name or "",
            name=obj.channel.name,
            description=obj.channel.description,
            is_default=obj.channel.is_default,
            count=obj.channel.count,
        ),
        hashtags=[HashtagData(id=t.id, ulid=t.ulid, name=t.name) for t in obj.hashtag.all()],
    )


def marshal_data(data: AudioData) -> Audio:
    return Audio(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        channel_id=data.channel.id,
        title=data.title,
        content=data.content,
        lyric=data.lyric,
        image=data.image,
        audio=data.audio,
        gain=data.gain,
        read=data.read,
        publish=data.publish,
        publish_at=data.publish_at,
    )
