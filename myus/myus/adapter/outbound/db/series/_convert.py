from django_ulid.models import ulid
from myus.db.models.series import Series
from myus.domain.series.data import SeriesData
from myus.utils.enum.media import MediaType


def convert_data(obj: Series) -> SeriesData:
    return SeriesData(
        id=obj.id,
        ulid=obj.ulid,
        channel_id=obj.channel_id,
        media_type=MediaType(obj.media_type),
        title=obj.title,
        media_ids=[sm.object_id for sm in obj.series_media.all()],
    )


def marshal_data(data: SeriesData) -> Series:
    return Series(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        channel_id=data.channel_id,
        media_type=data.media_type,
        title=data.title,
    )
