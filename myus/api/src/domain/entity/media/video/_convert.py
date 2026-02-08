from api.db.models.media import Video
from api.src.domain.interface.media.video.data import VideoData


def video_data(obj: Video) -> VideoData:
    return VideoData(
        id=obj.id,
        ulid=obj.ulid,
        channel_id=obj.channel_id,
        title=obj.title,
        content=obj.content,
        image=obj.image.name if obj.image else "",
        video=obj.video.name if obj.video else "",
        convert=obj.convert.name if obj.convert else "",
        read=obj.read,
        publish=obj.publish,
    )


def marshal_video(data: VideoData) -> Video:
    return Video(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid,
        channel_id=data.channel_id,
        title=data.title,
        content=data.content,
        image=data.image,
        video=data.video,
        convert=data.convert,
        read=data.read,
        publish=data.publish,
    )
