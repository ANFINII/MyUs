from myus.utils.common.result import Result, ValidationError
from .data import PaymentSellerData


def validate(obj: PaymentSellerData) -> Result[None, ValidationError]:
    if obj.user_id == 0:
        return Result.err(ValidationError("error.userRequired"))

    if len(obj.external_id) == 0:
        return Result.err(ValidationError("error.externalIdRequired"))

    return Result.ok(None)
