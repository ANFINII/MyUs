from myus.db.models.payment import BlogPurchase
from myus.domain.payment.purchase.data import BlogPurchaseData


def convert_data(obj: BlogPurchase) -> BlogPurchaseData:
    return BlogPurchaseData(
        id=obj.id,
        user_id=obj.user_id,
        blog_id=obj.blog_id,
        transaction_id=obj.transaction_id,
    )


def marshal_data(data: BlogPurchaseData) -> BlogPurchase:
    return BlogPurchase(
        id=data.id if data.id != 0 else None,
        user_id=data.user_id,
        blog_id=data.blog_id,
        transaction_id=data.transaction_id,
    )
