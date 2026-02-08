from api.db.models.media import Picture
from api.src.domain.interface.media.picture.data import PictureData


def picture_data(obj: Picture) -> PictureData:
    return PictureData(
        id=obj.id,
        ulid=obj.ulid,
        channel_id=obj.channel_id,
        title=obj.title,
        content=obj.content,
        image=obj.image.name if obj.image else "",
        read=obj.read,
        publish=obj.publish,
    )


def marshal_picture(data: PictureData) -> Picture:
    return Picture(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid,
        channel_id=data.channel_id,
        title=data.title,
        content=data.content,
        image=data.image,
        read=data.read,
        publish=data.publish,
    )
