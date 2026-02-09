from api.db.models.media import Comic
from api.src.domain.interface.media.comic.data import ComicData


def comic_data(obj: Comic) -> ComicData:
    return ComicData(
        id=obj.id,
        ulid=obj.ulid,
        channel_id=obj.channel_id,
        title=obj.title,
        content=obj.content,
        image=obj.image.name if obj.image else "",
        read=obj.read,
        publish=obj.publish,
        owner_id=obj.channel.owner_id,
        created=obj.created,
        updated=obj.updated,
        like_count=obj.like.count(),
        comment_count=obj.comment_count(),
    )


def marshal_comic(data: ComicData) -> Comic:
    return Comic(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid,
        channel_id=data.channel_id,
        title=data.title,
        content=data.content,
        image=data.image,
        read=data.read,
        publish=data.publish,
    )
