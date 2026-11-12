from myus.utils.common.result import Result, ValidationError
from .data import PayoutData


def validate(obj: PayoutData) -> Result[None, ValidationError]:
    if len(obj.external_id) == 0:
        return Result.err(ValidationError("error.externalIdRequired"))

    return Result.ok(None)
