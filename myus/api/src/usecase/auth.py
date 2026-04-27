import jwt
from dataclasses import replace
from datetime import date, datetime
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string
from api.db.models.user import User
from api.modules.logger import log
from api.src.domain.interface.user.data import MyPageData, PlanData, ProfileData, UserAllData, UserData, UserNotificationData, UserPlanData
from api.src.domain.interface.user.interface import UserInterface
from api.src.injectors.container import injector
from api.src.types.schema.auth import PasswordChangeIn, SignupIn
from api.utils.functions.encrypt import decrypt
from api.utils.functions.token import signup_token
from api.utils.functions.validation import has_email


def auth_check(request: HttpRequest) -> int | None:
    token = request.COOKIES.get("access_token")
    if token is None:
        return None

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
        user_id: int | None = payload["user_id"]
        if user_id is None:
            return None

        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None


def verify_user(user_id: int) -> bool:
    repository = injector.get(UserInterface)
    users = repository.bulk_get([user_id])
    if len(users) == 0:
        return False

    if not users[0].user.is_active:
        return False

    return True


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


def signup_send_email(email: str) -> str:
    if has_email(email):
        return "メールアドレスの形式が違います!"

    if User.objects.filter(email=email).exists():
        return "メールアドレスは既に登録されています!"

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
        return "メールの送信に失敗しました!"

    if settings.DEBUG:
        url = f"{settings.FRONTEND_URL}/account/signup?token={token}"
        log.info("Signup verify URL (dev)", url=url)

    return ""


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


def signup_user(input: SignupIn) -> bool:
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
            plan=PlanData(
                id=0,
                name="",
                stripe_api_id="",
                price=0,
                max_advertise=0,
                description="",
            ),
            customer_id="",
            subscription="",
            is_paid=False,
            start_date=None,
            end_date=None,
        ),
    )

    try:
        repository = injector.get(UserInterface)
        repository.bulk_save(objs=[user_data])
        return True
    except Exception as e:
        log.error("Signup error", exc=e)
        return False


PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 16


def change_password(user_id: int, input: PasswordChangeIn) -> str:
    try:
        old_password = decrypt(input.old_password)
        new_password1 = decrypt(input.new_password1)
        new_password2 = decrypt(input.new_password2)
    except Exception:
        log.error("Decrypt error")
        return "復号に失敗しました!"

    if new_password1 != new_password2:
        return "新規パスワードが一致しません!"

    if len(new_password1) < PASSWORD_MIN_LENGTH or len(new_password1) > PASSWORD_MAX_LENGTH:
        return "新規パスワードは英数字8~16文字で入力してください!"

    repository = injector.get(UserInterface)
    users = repository.bulk_get([user_id])
    if len(users) == 0:
        log.error("User not found", user_id=user_id)
        return "ユーザーが見つかりません!"

    user_data = users[0]
    if not check_password(old_password, user_data.user.password):
        return "現在のパスワードが違います!"

    new_user = replace(user_data.user, password=make_password(new_password1))
    new_data = replace(user_data, user=new_user)

    try:
        repository.bulk_save([new_data])
        return ""
    except Exception as e:
        log.error("change_password error", exc=e)
        return "パスワードの変更に失敗しました!"
