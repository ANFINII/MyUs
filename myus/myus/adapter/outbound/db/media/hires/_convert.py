from myus.db.models.media import Hires
from myus.domain.media.hires.data import HiresData


def convert_data(obj: Hires) -> HiresData:
    return HiresData(
        id=obj.id,
        audio_id=obj.audio_id,
        file=obj.file.name or "",
        sample_rate=obj.sample_rate,
        bit_depth=obj.bit_depth,
    )


def marshal_data(data: HiresData) -> Hires:
    return Hires(
        id=data.id if data.id != 0 else None,
        audio_id=data.audio_id,
        file=data.file,
        sample_rate=data.sample_rate,
        bit_depth=data.bit_depth,
    )
