from api.db.models.media import Music
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.media.music.data import MusicData


def music_data(obj: Music) -> MusicData:
    return MusicData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        lyric=obj.lyric,
        music=obj.music.name if obj.music else "",
        read=obj.read,
        download=obj.download,
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


def marshal_music(data: MusicData) -> Music:
    return Music(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid,
        channel_id=data.channel.id,
        title=data.title,
        content=data.content,
        lyric=data.lyric,
        music=data.music,
        read=data.read,
        download=data.download,
        publish=data.publish,
    )
