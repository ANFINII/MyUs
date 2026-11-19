from dataclasses import replace
from datetime import UTC, date, datetime
from typing import assert_never
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from myus.domain.payment.provider.data import CancelFailedData, CancelSuccessData
from myus.domain.user.data import MyPageData, ProfileData, UserAllData, UserData, UserNotificationData, UserPlanData
from myus.domain.user.interface import FilterOption, PageOption, SortOption, UserInterface
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import FatalError, NotFoundError, Result, ValidateError, ValidationError
from myus.utils.constants.auth import LOGIN_FAILURE_LIMIT
from myus.utils.enum.i18n import Locale
from myus.utils.enum.payment import CancelError
from myus.utils.enum.user import PlanName
from myus.utils.functions.auth import add_failure, clear_failures, get_failure_count
from myus.utils.functions.common import create_frontend_url
from myus.utils.functions.mail import send_template_mail
from myus.utils.functions.map import mail_locale
from myus.utils.functions.token import access_token, decode_token, is_revoked, password_reset_token, refresh_token, revoke, signup_token
from myus.utils.functions.transaction import atomic_result
from myus.utils.functions.validation import has_email, has_password, has_weak_password
from ._convert import get_active_user_data, is_same_password, create_user_data
from ..dto.user import PasswordChangeDTO, PasswordResetDTO, SignupDTO
from ..payment.core import cancel_subscription


@Result.shield_exception()
def verify_token(token: str, token_type: str) -> Result[int | None, FatalError]:
    payload = decode_token(token)
    if payload is None:
        return Result.ok(None)

    if payload.get("type") != token_type:
        log.warning("invalid token type", token_type=token_type)
        return Result.ok(None)

    user_id = payload.get("user_id")
    if not isinstance(user_id, int):
        return Result.ok(None)

    jti = payload.get("jti")
    if not isinstance(jti, str):
        return Result.ok(None)

    if is_revoked(jti):
        log.warning("token revoked", user_id=user_id)
        return Result.ok(None)

    ret = get_active_user_data(user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    user = ret.ok_value
    if user is None:
        log.warning("token user inactive", user_id=user_id)
        return Result.ok(None)

    if not is_same_password(payload.get("pwd"), user.user.password):
        log.warning("token invalidated by password change", user_id=user_id)
        return Result.ok(None)

    return Result.ok(user_id)


@Result.shield_exception()
def create_auth_tokens(user_id: int) -> Result[tuple[str, str] | None, FatalError]:
    ret = get_active_user_data(user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    user = ret.ok_value
    if user is None:
        return Result.ok(None)

    password_hash = user.user.password
    return Result.ok((access_token(user_id, password_hash), refresh_token(user_id, password_hash)))


@Result.shield_exception()
def login_user(username: str, password: str) -> Result[int | None, ValidateError]:
    if get_failure_count(username) >= LOGIN_FAILURE_LIMIT:
        log.warning("blocked: too many attempts", username=username)
        return Result.err(ValidationError("error.tooManyAttempts"))

    repo = injector.get(UserInterface)
    user_id_ret = repo.authenticate(username, password)
    if user_id_ret.is_err:
        return Result.err(user_id_ret.err_value)

    user_id = user_id_ret.ok_value
    if user_id is None:
        add_failure(username)
        return Result.ok(None)

    user_ret = get_active_user_data(user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        add_failure(username)
        return Result.ok(None)

    clear_failures(username)
    return Result.ok(user_id)


@Result.shield_exception()
def logout_user(access: str, refresh: str) -> Result[None, FatalError]:
    for token in [access, refresh]:
        payload = decode_token(token)
        if payload is None:
            continue

        jti = payload.get("jti")
        exp = payload.get("exp")
        if not isinstance(jti, str) or not isinstance(exp, int):
            continue

        revoke(jti, datetime.fromtimestamp(exp, tz=UTC))

    return Result.ok(None)


@Result.shield_exception()
def signup_send_email(email: str, locale: Locale) -> Result[str, FatalError]:
    if has_email(email):
        return Result.ok("error.emailInvalid")

    repo = injector.get(UserInterface)
    ret = repo.get_ids(FilterOption(email=email), SortOption(), PageOption())
    if ret.is_err:
        return Result.err(ret.err_value)

    user_ids = ret.ok_value
    if len(user_ids) > 0:
        return Result.ok("error.emailTaken")

    token = signup_token(email)
    url = f"{create_frontend_url(locale)}/account/signup?token={token}"
    mail = mail_locale(locale).value
    if not send_template_mail(f"registration/email/{mail}/account", {"action_url": url}, email):
        return Result.ok("error.mailSendFailed")

    if settings.DEBUG:
        log.info("verify URL (dev)", url=url)

    return Result.ok("")


def signup_verify_token(token: str) -> str | None:
    payload = decode_token(token)
    if payload is None:
        log.warning("invalid token")
        return None

    if payload.get("type") != "signup":
        log.warning("invalid token type")
        return None

    email = payload.get("email")
    if not isinstance(email, str) or len(email) == 0:
        log.warning("invalid token email")
        return None

    return email


@Result.shield_exception()
def signup_user(input: SignupDTO) -> Result[None, FatalError]:
    user_data = UserAllData(
        user=UserData(
            id=0,
            ulid="",
            avatar="",
            password=input.password1,
            email=input.email,
            username=input.username,
            nickname=input.nickname,
            is_active=True,
            is_staff=False,
            date_joined=datetime.now(),
        ),
        profile=ProfileData(
            last_name=input.last_name,
            first_name=input.first_name,
            gender=input.gender,
            birthday=date(year=input.year, month=input.month, day=input.day),
            phone="",
            country=input.country,
            postal_code="",
            prefecture="",
            city="",
            street="",
            introduction="",
        ),
        mypage=MyPageData(
            banner="",
            email="",
            content="",
            follower_count=0,
            following_count=0,
            measurement_id="",
            is_advertise=False,
        ),
        notification=UserNotificationData(
            is_video=False,
            is_music=False,
            is_blog=False,
            is_comic=False,
            is_picture=False,
            is_chat=False,
            is_follow=True,
            is_reply=True,
            is_like=True,
            is_views=True,
        ),
        user_plan=UserPlanData(
            plan=PlanName.FREE,
            is_paid=False,
            start_date=None,
            end_date=None,
        ),
    )

    create_ret = atomic_result(lambda: create_user_data(user_data, input.nickname))
    if create_ret.is_err:
        return Result.err(create_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def change_password(user_id: int, input: PasswordChangeDTO) -> Result[str, FatalError]:
    old_password = input.old_password
    password1 = input.password1
    password2 = input.password2
    if password1 != password2:
        return Result.ok("error.newPasswordMismatch")

    if has_password(password1):
        return Result.ok("error.newPasswordInvalid")

    repo = injector.get(UserInterface)
    users_ret = repo.bulk_get([user_id])
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    if len(users) == 0:
        log.error("not found", user_id=user_id)
        return Result.ok("error.userNotFound")

    user_data = users[0]
    user = user_data.user
    if not check_password(old_password, user.password):
        return Result.ok("error.currentPasswordWrong")

    if has_weak_password(password1, user.username, user.email, user.nickname):
        return Result.ok("error.passwordWeak")

    new_user = replace(user, password=make_password(password1))
    new_data = replace(user_data, user=new_user)

    save_ret = repo.bulk_save([new_data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok("")


@Result.shield_exception()
def password_reset_send_email(email: str, locale: Locale) -> Result[str, FatalError]:
    if has_email(email):
        return Result.ok("error.emailInvalid")

    repo = injector.get(UserInterface)
    ids_ret = repo.get_ids(FilterOption(email=email), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    user_ids = ids_ret.ok_value
    if len(user_ids) == 0:
        return Result.ok("")

    users_ret = repo.bulk_get(user_ids)
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    user_data = users[0]
    if not user_data.user.is_active:
        return Result.ok("")

    token = password_reset_token(user_data.user.id, email, user_data.user.password)
    url = f"{create_frontend_url(locale)}/account/reset/confirm?token={token}"
    mail = mail_locale(locale).value
    if not send_template_mail(f"registration/email/{mail}/reset", {"action_url": url, "nickname": user_data.user.nickname}, email):
        return Result.ok("error.mailSendFailed")

    if settings.DEBUG:
        log.info("reset URL (dev)", url=url)

    return Result.ok("")


@Result.shield_exception()
def password_reset_verify_token(token: str) -> Result[tuple[int, str] | None, FatalError]:
    payload = decode_token(token)
    if payload is None:
        log.warning("invalid token")
        return Result.ok(None)

    if payload.get("type") != "password_reset":
        log.warning("invalid token type")
        return Result.ok(None)

    user_id = payload.get("user_id")
    if not isinstance(user_id, int):
        log.warning("invalid token user_id")
        return Result.ok(None)

    email = payload.get("email")
    if not isinstance(email, str) or len(email) == 0:
        log.warning("invalid token email")
        return Result.ok(None)

    ret = get_active_user_data(user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    user = ret.ok_value
    if user is None:
        log.warning("not found", user_id=user_id)
        return Result.ok(None)

    if not is_same_password(payload.get("pwd"), user.user.password):
        log.warning("token already used", user_id=user_id)
        return Result.ok(None)

    return Result.ok((user_id, email))


@Result.shield_exception()
def reset_password(input: PasswordResetDTO) -> Result[str, FatalError]:
    verify_ret = password_reset_verify_token(input.token)
    if verify_ret.is_err:
        return Result.err(verify_ret.err_value)

    verified = verify_ret.ok_value
    if verified is None:
        return Result.ok("error.linkExpired")
    user_id, _ = verified

    password1 = input.password1
    password2 = input.password2
    if password1 != password2:
        return Result.ok("error.newPasswordMismatch")

    if has_password(password1):
        return Result.ok("error.newPasswordInvalid")

    repo = injector.get(UserInterface)
    users_ret = repo.bulk_get([user_id])
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    if len(users) == 0:
        log.error("not found", user_id=user_id)
        return Result.ok("error.userNotFound")

    user_data = users[0]
    user = user_data.user
    if has_weak_password(password1, user.username, user.email, user.nickname):
        return Result.ok("error.passwordWeak")

    new_user = replace(user, password=make_password(password1))
    new_data = replace(user_data, user=new_user)

    save_ret = repo.bulk_save([new_data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok("")


@Result.shield_exception()
def withdraw_user(user_id: int, password: str) -> Result[str, FatalError]:
    repo = injector.get(UserInterface)
    users_ret = repo.bulk_get([user_id])
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    if len(users) == 0:
        log.error("not found", user_id=user_id)
        return Result.ok("error.userNotFound")

    user_data = users[0]
    if not check_password(password, user_data.user.password):
        return Result.ok("error.passwordWrong")

    cancel_ret = cancel_subscription(user_id)
    if cancel_ret.is_err:
        match cancel_ret.err_value:
            case NotFoundError():
                log.info("no active subscription", user_id=user_id)
            case FatalError():
                return Result.err(cancel_ret.err_value)
            case _:
                assert_never(cancel_ret.err_value)
    else:
        cancellation = cancel_ret.ok_value
        match cancellation:
            case CancelSuccessData() | CancelFailedData(error=CancelError.NOT_FOUND):
                log.info("subscription canceled", user_id=user_id)
            case CancelFailedData(error=error, message=message):
                log.error("subscription cancel failed", user_id=user_id, error=error.value, message=message)
                return Result.ok("error.cancelFailed")
            case _:
                assert_never(cancellation)

    new_user = replace(user_data.user, is_active=False)
    new_data = replace(user_data, user=new_user)

    save_ret = repo.bulk_save([new_data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok("")
