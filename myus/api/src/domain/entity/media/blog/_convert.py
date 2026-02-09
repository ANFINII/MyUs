from api.db.models.media import Blog
from api.src.domain.interface.media.blog.data import BlogData


def blog_data(obj: Blog) -> BlogData:
    return BlogData(
        id=obj.id,
        ulid=obj.ulid,
        channel_id=obj.channel_id,
        title=obj.title,
        content=obj.content,
        richtext=obj.richtext,
        delta=obj.delta.html if obj.delta else "",
        image=obj.image.name if obj.image else "",
        read=obj.read,
        publish=obj.publish,
        owner_id=obj.channel.owner_id,
        created=obj.created,
        updated=obj.updated,
        like_count=obj.like.count(),
        comment_count=obj.comment_count(),
    )


def marshal_blog(data: BlogData) -> Blog:
    return Blog(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid,
        channel_id=data.channel_id,
        title=data.title,
        content=data.content,
        richtext=data.richtext,
        image=data.image,
        read=data.read,
        publish=data.publish,
    )
