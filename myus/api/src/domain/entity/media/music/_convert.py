from api.db.models.media import Music
from api.src.domain.interface.media.music.data import MusicData


def music_data(obj: Music) -> MusicData:
    return MusicData(
        id=obj.id,
        ulid=obj.ulid,
        channel_id=obj.channel_id,
        title=obj.title,
        content=obj.content,
        lyric=obj.lyric,
        music=obj.music.name if obj.music else "",
        read=obj.read,
        download=obj.download,
        publish=obj.publish,
    )


def marshal_music(data: MusicData) -> Music:
    return Music(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid,
        channel_id=data.channel_id,
        title=data.title,
        content=data.content,
        lyric=data.lyric,
        music=data.music,
        read=data.read,
        download=data.download,
        publish=data.publish,
    )
