from myus.domain.interface.payment.event.data import PaymentEventData
from myus.utils.common.result import Result, ValidationError


def validate(obj: PaymentEventData) -> Result[None, ValidationError]:
    if len(obj.event_id) == 0:
        return Result.err(ValidationError("error.eventIdRequired"))

    if len(obj.external_id) == 0:
        return Result.err(ValidationError("error.externalIdRequired"))

    return Result.ok(None)
