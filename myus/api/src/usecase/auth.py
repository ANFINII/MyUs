import jwt
from dataclasses import replace
from datetime import date, datetime
from typing import assert_never
from django_ulid.models import ulid
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.http import HttpRequest
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
from api.utils.functions.encrypt import decrypt
from api.utils.functions.token import password_reset_token, signup_token
from api.utils.functions.validation import has_email


@Result.shield_exception()
def auth_check(request: HttpRequest) -> Result[int | None, FatalError]:
    token = request.COOKIES.get("access_token")
    if token is None:
        return Result.ok(None)

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return Result.ok(None)
    except jwt.exceptions.DecodeError:
        return Result.ok(None)

    if payload.get("type") != "access":
        log.warning("アクセストークンのタイプが不正です")
        return Result.ok(None)

    user_id = payload.get("user_id")
    if user_id is None:
        return Result.ok(None)

    ret = verify_user(user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    is_verified = ret.ok_value
    if not is_verified:
        log.warning("無効なユーザーのトークンです", user_id=user_id)
        return Result.ok(None)

    return Result.ok(user_id)


@Result.shield_exception()
def verify_user(user_id: int) -> Result[bool, FatalError]:
    repo = injector.get(UserInterface)
    ret = repo.bulk_get([user_id])
    if ret.is_err:
        return Result.err(ret.err_value)

    users = ret.ok_value
    if len(users) == 0:
        return Result.ok(False)

    if not users[0].user.is_active:
        return Result.ok(False)

    return Result.ok(True)


def login_user(username: str, password: str) -> int | None:
    try:
        decrypted_username = decrypt(username)
        decrypted_password = decrypt(password)
    except Exception:
        log.error("Decrypt error")
        return None

    user = authenticate(username=decrypted_username, password=decrypted_password)
    if not user:
        user = authenticate(email=decrypted_username, password=decrypted_password)

    if not user:
        return None

    if not user.is_active:
        return None

    return user.id


@Result.shield_exception()
def signup_send_email(email: str) -> Result[str, FatalError]:
    if has_email(email):
        return Result.ok("メールアドレスの形式が違います!")

    repo = injector.get(UserInterface)
    ret = repo.get_ids(FilterOption(email=email))
    if ret.is_err:
        return Result.err(ret.err_value)

    user_ids = ret.ok_value
    if len(user_ids) > 0:
        return Result.ok("メールアドレスは既に登録されています!")

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
        return Result.ok("メールの送信に失敗しました!")

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

    user_repo = injector.get(UserInterface)
    user_ret = user_repo.bulk_save(objs=[user_data])
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user_ids = user_ret.ok_value
    channel_repo = injector.get(ChannelInterface)
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
        log.error("Default channel create error", error=channel_ret.err_value.error_message, user_id=user_ids[0])

    return Result.ok(None)


PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 16


@Result.shield_exception()
def change_password(user_id: int, input: PasswordChangeIn) -> Result[str, FatalError]:
    try:
        old_password = decrypt(input.old_password)
        password1 = decrypt(input.password1)
        password2 = decrypt(input.password2)
    except Exception:
        log.error("Decrypt error")
        return Result.ok("復号に失敗しました!")

    if password1 != password2:
        return Result.ok("新規パスワードが一致しません!")

    if len(password1) < PASSWORD_MIN_LENGTH or len(password1) > PASSWORD_MAX_LENGTH:
        return Result.ok("新規パスワードは英数字8~16文字で入力してください!")

    repo = injector.get(UserInterface)
    users_ret = repo.bulk_get([user_id])
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    if len(users) == 0:
        log.error("User not found", user_id=user_id)
        return Result.ok("ユーザーが見つかりません!")

    user_data = users[0]
    if not check_password(old_password, user_data.user.password):
        return Result.ok("現在のパスワードが違います!")

    new_user = replace(user_data.user, password=make_password(password1))
    new_data = replace(user_data, user=new_user)

    save_ret = repo.bulk_save([new_data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok("")


@Result.shield_exception()
def password_reset_send_email(email: str) -> Result[str, FatalError]:
    if has_email(email):
        return Result.ok("メールアドレスの形式が違います!")

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

    token = password_reset_token(user_data.user.id, email)
    subject = render_to_string("registration/email/reset/subject.txt").strip()
    message = render_to_string(
        "registration/email/reset/message.txt",
        {"frontend_url": settings.FRONTEND_URL, "token": token, "nickname": user_data.user.nickname},
    )

    try:
        send_mail(subject, message, None, [email])
    except Exception as e:
        log.error("Password reset email send error", exc=e)
        return Result.ok("メールの送信に失敗しました!")

    if settings.DEBUG:
        url = f"{settings.FRONTEND_URL}/account/reset/confirm?token={token}"
        log.info("Password reset URL (dev)", url=url)

    return Result.ok("")


def password_reset_verify_token(token: str) -> tuple[int, str] | None:
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        log.warning("Password reset token expired")
        return None
    except jwt.exceptions.DecodeError:
        log.warning("Password reset token decode error")
        return None

    if payload.get("type") != "password_reset":
        log.warning("Invalid password reset token type")
        return None

    user_id = payload.get("user_id")
    if not isinstance(user_id, int):
        log.warning("Invalid password reset token user_id")
        return None

    email = payload.get("email")
    if not isinstance(email, str) or len(email) == 0:
        log.warning("Invalid password reset token email")
        return None

    return (user_id, email)


@Result.shield_exception()
def reset_password(input: PasswordResetIn) -> Result[str, FatalError]:
    result = password_reset_verify_token(input.token)
    if result is None:
        return Result.ok("リンクの有効期限が切れています!")
    user_id, _ = result

    try:
        password1 = decrypt(input.password1)
        password2 = decrypt(input.password2)
    except Exception:
        log.error("Decrypt error")
        return Result.ok("復号に失敗しました!")

    if password1 != password2:
        return Result.ok("新規パスワードが一致しません!")

    if len(password1) < PASSWORD_MIN_LENGTH or len(password1) > PASSWORD_MAX_LENGTH:
        return Result.ok("新規パスワードは英数字8~16文字で入力してください!")

    repo = injector.get(UserInterface)
    users_ret = repo.bulk_get([user_id])
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    if len(users) == 0:
        log.error("User not found", user_id=user_id)
        return Result.ok("ユーザーが見つかりません!")

    user_data = users[0]
    new_user = replace(user_data.user, password=make_password(password1))
    new_data = replace(user_data, user=new_user)

    save_ret = repo.bulk_save([new_data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok("")


@Result.shield_exception()
def withdraw_user(user_id: int, input: WithdrawalIn) -> Result[str, FatalError]:
    try:
        password = decrypt(input.password)
    except Exception:
        log.error("Decrypt error")
        return Result.ok("復号に失敗しました!")

    repo = injector.get(UserInterface)
    users_ret = repo.bulk_get([user_id])
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    if len(users) == 0:
        log.error("User not found", user_id=user_id)
        return Result.ok("ユーザーが見つかりません!")

    user_data = users[0]
    if not check_password(password, user_data.user.password):
        return Result.ok("パスワードが違います!")

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
                return Result.ok("解約処理に失敗しました。時間をおいて再度お試しください!")
            case _:
                assert_never(cancellation)

    new_user = replace(user_data.user, is_active=False)
    new_data = replace(user_data, user=new_user)

    save_ret = repo.bulk_save([new_data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok("")
