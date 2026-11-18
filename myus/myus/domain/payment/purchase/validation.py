from myus.utils.common.result import Result, ValidationError
from .data import BlogPurchaseData


def validate(obj: BlogPurchaseData) -> Result[None, ValidationError]:
    if obj.user_id == 0:
        return Result.err(ValidationError("error.userRequired"))

    if obj.blog_id == 0:
        return Result.err(ValidationError("error.blogRequired"))

    if obj.transaction_id == 0:
        return Result.err(ValidationError("error.transactionRequired"))

    return Result.ok(None)
