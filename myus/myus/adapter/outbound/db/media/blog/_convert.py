from django_ulid.models import ulid
from myus.db.models.media import Blog
from myus.domain.channel.data import ChannelData
from myus.domain.hashtag.data import HashtagData
from myus.domain.media.blog.data import BlogData
from myus.domain.payment.data import Money
from myus.utils.enum.i18n import Currency


def convert_data(obj: Blog) -> BlogData:
    assert hasattr(obj, "like_count"), "like_count is required"
    category = next(iter(obj.category.all()), None)
    return BlogData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        richtext=obj.richtext,
        paid_richtext=obj.paid_richtext,
        price=Money(amount=obj.price_amount, currency=Currency(obj.price_currency)),
        image=obj.image.name or "",
        read=obj.read,
        like=obj.like_count,
        publish=obj.publish,
        publish_at=obj.publish_at,
        is_promotion=obj.is_promotion,
        created=obj.created,
        updated=obj.updated,
        category_ulid=category.ulid if category is not None else "",
        channel=ChannelData(
            id=obj.channel.id,
            ulid=obj.channel.ulid,
            owner_id=obj.channel.owner_id,
            owner_ulid=obj.channel.owner.ulid,
            avatar=obj.channel.avatar.name or "",
            name=obj.channel.name,
            description=obj.channel.description,
            is_default=obj.channel.is_default,
            count=obj.channel.count,
        ),
        hashtags=[HashtagData(id=t.id, ulid=t.ulid, name=t.name) for t in obj.hashtag.all()],
    )


def marshal_data(data: BlogData) -> Blog:
    return Blog(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        channel_id=data.channel.id,
        title=data.title,
        content=data.content,
        richtext=data.richtext,
        paid_richtext=data.paid_richtext,
        price_amount=data.price.amount,
        price_currency=data.price.currency,
        image=data.image,
        read=data.read,
        publish=data.publish,
        publish_at=data.publish_at,
        is_promotion=data.is_promotion,
    )
