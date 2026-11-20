from django_ulid.models import ulid
from myus.db.models.media import Audio, Hires
from myus.domain.channel.data import ChannelData
from myus.domain.hashtag.data import HashtagData
from myus.domain.media.audio.data import AudioData, HiresData
from myus.utils.enum.media import EncodeStatus


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
        encode_status=EncodeStatus(obj.encode_status),
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
        hires=hires_data(obj.hires) if hasattr(obj, "hires") else None,
    )


def hires_data(obj: Hires) -> HiresData:
    return HiresData(
        id=obj.id,
        file=obj.file.name or "",
        sample_rate=obj.sample_rate,
        bit_depth=obj.bit_depth,
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
        encode_status=data.encode_status,
        read=data.read,
        publish=data.publish,
        publish_at=data.publish_at,
    )


def marshal_hires_data(data: HiresData, audio_id: int) -> Hires:
    return Hires(
        id=data.id if data.id != 0 else None,
        audio_id=audio_id,
        file=data.file,
        sample_rate=data.sample_rate,
        bit_depth=data.bit_depth,
    )
