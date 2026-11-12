from myus.src.domain.interface.payment.subscription.data import SubscriptionData
from myus.utils.common.result import Result, ValidationError
from myus.utils.plan import get_plan


def validate(obj: SubscriptionData) -> Result[None, ValidationError]:
    if obj.payment_customer_id == 0:
        return Result.err(ValidationError("error.customerRequired"))

    if len(obj.external_id) == 0:
        return Result.err(ValidationError("error.externalIdRequired"))

    if get_plan(obj.product_code) is None:
        return Result.err(ValidationError("error.planUnknown"))

    if obj.price.amount < 0:
        return Result.err(ValidationError("error.priceRange"))

    return Result.ok(None)
