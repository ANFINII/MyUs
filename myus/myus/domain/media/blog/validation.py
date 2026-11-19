from myus.utils.common.result import Result, ValidationError
from .data import BlogData


BLOG_TITLE_MAX_LENGTH = 100


def validate(obj: BlogData) -> Result[None, ValidationError]:
    if len(obj.title) > BLOG_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    return Result.ok(None)
