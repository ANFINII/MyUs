from myus.utils.common.result import Result, ValidationError
from .data import PurchaseData


def validate(obj: PurchaseData) -> Result[None, ValidationError]:
    if obj.user_id == 0:
        return Result.err(ValidationError("error.userRequired"))

    if obj.product_id == 0:
        return Result.err(ValidationError("error.productRequired"))

    if obj.transaction_id == 0:
        return Result.err(ValidationError("error.transactionRequired"))

    return Result.ok(None)
