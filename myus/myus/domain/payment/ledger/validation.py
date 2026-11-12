from myus.utils.common.result import Result, ValidationError
from .data import LedgerEntryData


def validate(obj: LedgerEntryData) -> Result[None, ValidationError]:
    if obj.transaction_id == 0:
        return Result.err(ValidationError("error.transactionRequired"))

    if obj.event_id == 0:
        return Result.err(ValidationError("error.eventRequired"))

    if len(obj.external_id) == 0:
        return Result.err(ValidationError("error.externalIdRequired"))

    return Result.ok(None)
