import hmac
import jwt
from dataclasses import replace
from datetime import date, datetime
from typing import assert_never
from django_ulid.models import ulid
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string
from api.modules.logger import log
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.channel.interface import ChannelInterface
from api.src.domain.interface.payment.provider.data import CancelFailed, CancelSuccess
from api.src.domain.interface.user.data import MyPageData, ProfileData, UserAllData, UserData, UserNotificationData, UserPlanData
from api.utils.enum.user import PlanName
from api.src.domain.interface.user.interface import FilterOption, UserInterface
from api.src.injectors.container import injector
from api.src.types.schema.auth import PasswordChangeIn, PasswordResetIn, SignupIn, WithdrawalIn
from api.src.usecase.payment import cancel_subscription
from api.utils.common.result import FatalError, NotFoundError, Result
from api.utils.enum.payment import CancelError
from api.utils.functions.token import access_token, password_fingerprint, password_reset_token, refresh_token, signup_token
from api.utils.functions.validation import PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH, has_email


@Result.shield_exception()
def verify_token(token: str, token_type: str) -> Result[int | None, FatalError]:
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return Result.ok(None)
    except jwt.exceptions.DecodeError:
        return Result.ok(None)

    if payload.get("type") != token_type:
        log.warning("トークンのタイプが不正です", token_type=token_type)
        return Result.ok(None)

    user_id = payload.get("user_id")
    if not isinstance(user_id, int):
        return Result.ok(None)

    ret = get_active_user(user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    user = ret.ok_value
    if user is None:
        log.warning("無効なユーザーのトークンです", user_id=user_id)
        return Result.ok(None)

    if not is_same_password(payload.get("pwd"), user.user.password):
        log.warning("パスワードが変わったため無効なトークンです", user_id=user_id)
        return Result.ok(None)

    return Result.ok(user_id)


@Result.shield_exception()
def get_active_user(user_id: int) -> Result[UserAllData | None, FatalError]:
    repo = injector.get(UserInterface)
    ret = repo.bulk_get([user_id])
    if ret.is_err:
        return Result.err(ret.err_value)

    users = ret.ok_value
    if len(users) == 0 or not users[0].user.is_active:
        return Result.ok(None)

    return Result.ok(users[0])


def is_same_password(fingerprint: object, password_hash: str) -> bool:
    if not isinstance(fingerprint, str):
        return False
    return hmac.compare_digest(fingerprint, password_fingerprint(password_hash))


@Result.shield_exception()
def create_auth_tokens(user_id: int) -> Result[tuple[str, str] | None, FatalError]:
    ret = get_active_user(user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    user = ret.ok_value
    if user is None:
        return Result.ok(None)

    password_hash = user.user.password
    return Result.ok((access_token(user_id, password_hash), refresh_token(user_id, password_hash)))


@Result.shield_exception()
def login_user(username: str, password: str) -> Result[int | None, FatalError]:
    repo = injector.get(UserInterface)
    user_id_ret = repo.authenticate(username, password)
    if user_id_ret.is_err:
        return Result.err(user_id_ret.err_value)

    user_id = user_id_ret.ok_value
    if user_id is None:
        return Result.ok(None)

    user_ret = get_active_user(user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        return Result.ok(None)

    return Result.ok(user_id)


@Result.shield_exception()
def signup_send_email(email: str) -> Result[str, FatalError]:
    if has_email(email):
        return Result.ok("error.emailInvalid")

    repo = injector.get(UserInterface)
    ret = repo.get_ids(FilterOption(email=email))
    if ret.is_err:
        return Result.err(ret.err_value)

    user_ids = ret.ok_value
    if len(user_ids) > 0:
        return Result.ok("error.emailTaken")

    token = signup_token(email)
    subject = render_to_string("registration/email/account/subject.txt").strip()
    message = render_to_string(
        "registration/email/account/message.txt",
        {"frontend_url": settings.FRONTEND_URL, "token": token},
    )

    try:
        send_mail(subject, message, None, [email])
    except Exception as e:
        log.error("Signup email send error", exc=e)
        return Result.ok("error.mailSendFailed")

    if settings.DEBUG:
        url = f"{settings.FRONTEND_URL}/account/signup?token={token}"
        log.info("Signup verify URL (dev)", url=url)

    return Result.ok("")


def signup_verify_token(token: str) -> str | None:
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        log.warning("Signup token expired")
        return None
    except jwt.exceptions.DecodeError:
        log.warning("Signup token decode error")
        return None

    if payload.get("type") != "signup":
        log.warning("Invalid signup token type")
        return None

    email = payload.get("email")
    if not isinstance(email, str) or len(email) == 0:
        log.warning("Invalid signup token email")
        return None

    return email


@Result.shield_exception()
def signup_user(input: SignupIn) -> Result[None, FatalError]:
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
            country_code="",
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
            tag_manager_id="",
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
            customer_id="",
            subscription="",
            is_paid=False,
            start_date=None,
            end_date=None,
        ),
    )

    repo = injector.get(UserInterface)
    channel_repo = injector.get(ChannelInterface)
    with transaction.atomic():
        user_ret = repo.bulk_save(objs=[user_data])
        if user_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(user_ret.err_value)

        user_ids = user_ret.ok_value
        channel_ret = channel_repo.bulk_save([ChannelData(
            id=0,
            ulid=str(ulid.new()),
            owner_id=user_ids[0],
            owner_ulid="",
            avatar="",
            name=input.nickname,
            description="",
            is_default=True,
            count=0,
        )])
        if channel_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(channel_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def change_password(user_id: int, input: PasswordChangeIn) -> Result[str, FatalError]:
    old_password = input.old_password
    password1 = input.password1
    password2 = input.password2
    if password1 != password2:
        return Result.ok("error.newPasswordMismatch")

    if len(password1) < PASSWORD_MIN_LENGTH or len(password1) > PASSWORD_MAX_LENGTH:
        return Result.ok("error.newPasswordInvalid")

    repo = injector.get(UserInterface)
    users_ret = repo.bulk_get([user_id])
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    if len(users) == 0:
        log.error("User not found", user_id=user_id)
        return Result.ok("error.userNotFound")

    user_data = users[0]
    if not check_password(old_password, user_data.user.password):
        return Result.ok("error.currentPasswordWrong")

    new_user = replace(user_data.user, password=make_password(password1))
    new_data = replace(user_data, user=new_user)

    save_ret = repo.bulk_save([new_data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok("")


@Result.shield_exception()
def password_reset_send_email(email: str) -> Result[str, FatalError]:
    if has_email(email):
        return Result.ok("error.emailInvalid")

    repo = injector.get(UserInterface)
    ids_ret = repo.get_ids(FilterOption(email=email))
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
    subject = render_to_string("registration/email/reset/subject.txt").strip()
    message = render_to_string(
        "registration/email/reset/message.txt",
        {"frontend_url": settings.FRONTEND_URL, "token": token, "nickname": user_data.user.nickname},
    )

    try:
        send_mail(subject, message, None, [email])
    except Exception as e:
        log.error("Password reset email send error", exc=e)
        return Result.ok("error.mailSendFailed")

    if settings.DEBUG:
        url = f"{settings.FRONTEND_URL}/account/reset/confirm?token={token}"
        log.info("Password reset URL (dev)", url=url)

    return Result.ok("")


@Result.shield_exception()
def password_reset_verify_token(token: str) -> Result[tuple[int, str] | None, FatalError]:
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        log.warning("Password reset token expired")
        return Result.ok(None)
    except jwt.exceptions.DecodeError:
        log.warning("Password reset token decode error")
        return Result.ok(None)

    if payload.get("type") != "password_reset":
        log.warning("Invalid password reset token type")
        return Result.ok(None)

    user_id = payload.get("user_id")
    if not isinstance(user_id, int):
        log.warning("Invalid password reset token user_id")
        return Result.ok(None)

    email = payload.get("email")
    if not isinstance(email, str) or len(email) == 0:
        log.warning("Invalid password reset token email")
        return Result.ok(None)

    ret = get_active_user(user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    user = ret.ok_value
    if user is None:
        log.warning("Password reset token user not found", user_id=user_id)
        return Result.ok(None)

    if not is_same_password(payload.get("pwd"), user.user.password):
        log.warning("Password reset token already used", user_id=user_id)
        return Result.ok(None)

    return Result.ok((user_id, email))


@Result.shield_exception()
def reset_password(input: PasswordResetIn) -> Result[str, FatalError]:
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

    if len(password1) < PASSWORD_MIN_LENGTH or len(password1) > PASSWORD_MAX_LENGTH:
        return Result.ok("error.newPasswordInvalid")

    repo = injector.get(UserInterface)
    users_ret = repo.bulk_get([user_id])
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    if len(users) == 0:
        log.error("User not found", user_id=user_id)
        return Result.ok("error.userNotFound")

    user_data = users[0]
    new_user = replace(user_data.user, password=make_password(password1))
    new_data = replace(user_data, user=new_user)

    save_ret = repo.bulk_save([new_data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok("")


@Result.shield_exception()
def withdraw_user(user_id: int, input: WithdrawalIn) -> Result[str, FatalError]:
    password = input.password
    repo = injector.get(UserInterface)
    users_ret = repo.bulk_get([user_id])
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    if len(users) == 0:
        log.error("User not found", user_id=user_id)
        return Result.ok("error.userNotFound")

    user_data = users[0]
    if not check_password(password, user_data.user.password):
        return Result.ok("error.passwordWrong")

    cancel_ret = cancel_subscription(user_id)
    if cancel_ret.is_err:
        match cancel_ret.err_value:
            case NotFoundError():
                log.info("Withdraw without active subscription", user_id=user_id)
            case FatalError():
                return Result.err(cancel_ret.err_value)
            case _:
                assert_never(cancel_ret.err_value)
    else:
        cancellation = cancel_ret.ok_value
        match cancellation:
            case CancelSuccess() | CancelFailed(error=CancelError.NOT_FOUND):
                log.info("Withdraw subscription canceled", user_id=user_id)
            case CancelFailed(error=error, message=message):
                log.error("Withdraw subscription cancel failed", user_id=user_id, error=error.value, message=message)
                return Result.ok("error.cancelFailed")
            case _:
                assert_never(cancellation)

    new_user = replace(user_data.user, is_active=False)
    new_data = replace(user_data, user=new_user)

    save_ret = repo.bulk_save([new_data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok("")
