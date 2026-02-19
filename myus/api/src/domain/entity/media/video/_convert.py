from api.db.models.media import Video
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.media.video.data import VideoData


def video_data(obj: Video) -> VideoData:
    return VideoData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=obj.image.name if obj.image else "",
        video=obj.video.name if obj.video else "",
        convert=obj.convert.name if obj.convert else "",
        read=obj.read,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        like_count=obj.like.count(),
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
    )


def marshal_video(data: VideoData) -> Video:
    return Video(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid,
        channel_id=data.channel.id,
        title=data.title,
        content=data.content,
        image=data.image,
        video=data.video,
        convert=data.convert,
        read=data.read,
        publish=data.publish,
    )
