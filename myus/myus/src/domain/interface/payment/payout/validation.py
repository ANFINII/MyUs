from myus.src.domain.interface.payment.payout.data import PayoutData
from myus.utils.common.result import Result, ValidationError


def validate(obj: PayoutData) -> Result[None, ValidationError]:
    if len(obj.external_id) == 0:
        return Result.err(ValidationError("error.externalIdRequired"))

    return Result.ok(None)
