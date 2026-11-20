from myus.db.models.media import AudioHires
from myus.domain.media.hires.data import AudioHiresData


def convert_data(obj: AudioHires) -> AudioHiresData:
    return AudioHiresData(
        id=obj.id,
        audio_id=obj.audio_id,
        file=obj.file.name or "",
        sample_rate=obj.sample_rate,
        bit_depth=obj.bit_depth,
    )


def marshal_data(data: AudioHiresData) -> AudioHires:
    return AudioHires(
        id=data.id if data.id != 0 else None,
        audio_id=data.audio_id,
        file=data.file,
        sample_rate=data.sample_rate,
        bit_depth=data.bit_depth,
    )
