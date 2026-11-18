from myus.utils.common.result import Result, ValidationError
from .data import BlogData


BLOG_TITLE_MAX_LENGTH = 100
BLOG_PRICE_MIN = 100
BLOG_PRICE_MAX = 50000


def validate(obj: BlogData) -> Result[None, ValidationError]:
    if len(obj.title) > BLOG_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.paid_text) > 0 and not BLOG_PRICE_MIN <= obj.price.amount <= BLOG_PRICE_MAX:
        return Result.err(ValidationError("error.priceRange"))

    if len(obj.paid_text) == 0 and obj.price.amount != 0:
        return Result.err(ValidationError("error.paidTextRequired"))

    return Result.ok(None)
