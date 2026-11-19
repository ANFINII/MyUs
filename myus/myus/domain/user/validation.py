from myus.utils.common.result import Result, ValidationError
from myus.utils.functions.validation import has_email, has_username, has_number, has_phone, has_postal_code, has_measurement_id
from .data import UserAllData


def validate(obj: UserAllData) -> Result[None, ValidationError]:
    if has_email(obj.user.email):
        return Result.err(ValidationError("error.emailInvalid"))

    if has_username(obj.user.username):
        return Result.err(ValidationError("error.usernameInvalid"))

    if has_number(obj.profile.last_name):
        return Result.err(ValidationError("error.lastNameInvalid"))

    if has_number(obj.profile.first_name):
        return Result.err(ValidationError("error.firstNameInvalid"))

    if len(obj.profile.phone) > 0 and has_phone(obj.profile.phone):
        return Result.err(ValidationError("error.phoneInvalid"))

    if len(obj.profile.postal_code) > 0 and has_postal_code(obj.profile.postal_code):
        return Result.err(ValidationError("error.postalCodeInvalid"))

    if len(obj.mypage.email) > 0 and has_email(obj.mypage.email):
        return Result.err(ValidationError("error.emailInvalid"))

    if len(obj.mypage.measurement_id) > 0 and has_measurement_id(obj.mypage.measurement_id):
        return Result.err(ValidationError("error.measurementIdInvalid"))

    return Result.ok(None)
