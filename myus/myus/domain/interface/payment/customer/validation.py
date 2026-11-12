from myus.domain.interface.payment.customer.data import PaymentCustomerData
from myus.utils.common.result import Result, ValidationError


def validate(obj: PaymentCustomerData) -> Result[None, ValidationError]:
    if obj.user_id == 0:
        return Result.err(ValidationError("error.userRequired"))

    if len(obj.external_id) == 0:
        return Result.err(ValidationError("error.externalIdRequired"))

    return Result.ok(None)
