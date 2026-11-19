from myus.utils.common.result import Result, ValidationError
from .data import ProjectionProgressData


def validate(obj: ProjectionProgressData) -> Result[None, ValidationError]:
    if len(obj.aggregate_type) == 0 or len(obj.aggregate_id) == 0:
        return Result.err(ValidationError("error.aggregateRequired"))

    if obj.last_applied_seq == 0:
        return Result.err(ValidationError("error.seqRequired"))

    return Result.ok(None)
