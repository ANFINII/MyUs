from django_ulid.models import ulid
from myus.db.models.playlist import Playlist
from myus.domain.playlist.data import PlaylistData


def convert_data(obj: Playlist) -> PlaylistData:
    return PlaylistData(
        id=obj.id,
        ulid=obj.ulid,
        author_id=obj.author_id,
        title=obj.title,
        description=obj.description,
        image=str(obj.image),
        publish=obj.publish,
        audio_ids=[pm.audio_id for pm in obj.playlist_audios.all()],
        created=obj.created,
        updated=obj.updated,
    )


def marshal_data(data: PlaylistData) -> Playlist:
    return Playlist(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        author_id=data.author_id,
        title=data.title,
        description=data.description,
        image=data.image,
        publish=data.publish,
    )
