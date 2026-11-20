from typing import assert_never
from myus.utils.common.result import Result, ValidationError
from myus.utils.enum.payment import ProductType
from .data import ProductData


BLOG_PRICE_MIN = 300
BLOG_PRICE_MAX = 50000
HIRES_PRICE_MIN = 300
HIRES_PRICE_MAX = 600
COMIC_PRICE_MIN = 300
COMIC_PRICE_MAX = 50000


def price_range(product_type: ProductType) -> tuple[int, int]:
    match product_type:
        case ProductType.BLOG:
            return BLOG_PRICE_MIN, BLOG_PRICE_MAX
        case ProductType.HIRES:
            return HIRES_PRICE_MIN, HIRES_PRICE_MAX
        case ProductType.COMIC:
            return COMIC_PRICE_MIN, COMIC_PRICE_MAX
        case _:
            assert_never(product_type)


def validate(obj: ProductData) -> Result[None, ValidationError]:
    if obj.seller_id == 0:
        return Result.err(ValidationError("error.sellerRequired"))

    if obj.object_id == 0:
        return Result.err(ValidationError("error.objectRequired"))

    price_min, price_max = price_range(obj.product_type)
    if not price_min <= obj.price.amount <= price_max:
        return Result.err(ValidationError("error.priceRange"))

    return Result.ok(None)
