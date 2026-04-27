from django_ulid.models import ulid
from api.db.models.media import Comic
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.hashtag.data import HashtagData
from api.src.domain.interface.media.comic.data import ComicData


def convert_data(obj: Comic) -> ComicData:
    category = obj.category.first()
    assert category is not None, "Category is required"
    return ComicData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=obj.image.name if obj.image else "",
        pages=[p.image.name for p in obj.comic.all() if p.image],
        read=obj.read,
        like=obj.like.count(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        channel=ChannelData(
            id=obj.channel.id,
            ulid=obj.channel.ulid,
            owner_id=obj.channel.owner_id,
            owner_ulid=obj.channel.owner.ulid,
            avatar=obj.channel.avatar.name if obj.channel.avatar else "",
            name=obj.channel.name,
            description=obj.channel.description,
            is_default=obj.channel.is_default,
            count=obj.channel.count,
        ),
        category_ulid=category.ulid,
        hashtags=[HashtagData(id=ch.hashtag.id, ulid=ch.hashtag.ulid, name=ch.hashtag.name) for ch in obj.comic_hashtags.all()],
    )


def marshal_data(data: ComicData) -> Comic:
    return Comic(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        channel_id=data.channel.id,
        title=data.title,
        content=data.content,
        image=data.image,
        read=data.read,
        publish=data.publish,
    )
