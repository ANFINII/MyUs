from myus.src.domain.interface.payment.transaction.data import TransactionData
from myus.utils.common.result import Result, ValidationError


TAX_RATE_MAX = 100
RECEIPT_NUMBER_MAX_LENGTH = 30


def validate(obj: TransactionData) -> Result[None, ValidationError]:
    if obj.payment_customer_id == 0:
        return Result.err(ValidationError("error.customerRequired"))

    if len(obj.external_id) == 0:
        return Result.err(ValidationError("error.externalIdRequired"))

    if not 0 <= obj.tax_rate <= TAX_RATE_MAX:
        return Result.err(ValidationError("error.taxRateRange"))

    if len(obj.receipt_number) > RECEIPT_NUMBER_MAX_LENGTH:
        return Result.err(ValidationError("error.receiptNumberLength"))

    return Result.ok(None)
