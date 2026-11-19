from myus.db.models.media import MusicHires
from myus.domain.media.hires.data import MusicHiresData


def convert_data(obj: MusicHires) -> MusicHiresData:
    return MusicHiresData(
        id=obj.id,
        music_id=obj.music_id,
        file=obj.file.name or "",
        sample_rate=obj.sample_rate,
        bit_depth=obj.bit_depth,
    )


def marshal_data(data: MusicHiresData) -> MusicHires:
    return MusicHires(
        id=data.id if data.id != 0 else None,
        music_id=data.music_id,
        file=data.file,
        sample_rate=data.sample_rate,
        bit_depth=data.bit_depth,
    )
