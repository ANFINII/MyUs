from django_ulid.models import ulid
from api.db.models.common import Advertise
from api.src.domain.interface.advertise.data import AdvertiseData


def convert_data(obj: Advertise) -> AdvertiseData:
    return AdvertiseData(
        id=obj.id,
        ulid=obj.ulid,
        author_id=obj.author_id,
        title=obj.title,
        url=obj.url,
        content=obj.content,
        image=obj.image.name if obj.image else "",
        video=obj.video.name if obj.video else "",
        read=obj.read,
        type=obj.type,
        period=obj.period,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
    )


def marshal_data(data: AdvertiseData) -> Advertise:
    return Advertise(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        author_id=data.author_id,
        title=data.title,
        url=data.url,
        content=data.content,
        image=data.image,
        video=data.video,
        read=data.read,
        type=data.type,
        period=data.period,
        publish=data.publish,
    )
