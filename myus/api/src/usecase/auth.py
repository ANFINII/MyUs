import jwt
from datetime import date, datetime
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpRequest
from api.modules.logger import log
from api.src.domain.interface.user.data import MyPageData, PlanData, ProfileData, UserAllData, UserData, UserNotificationData, UserPlanData
from api.src.domain.interface.user.interface import UserInterface
from api.src.injectors.container import injector
from api.src.types.schema.auth import SignupIn
from api.utils.functions.encrypt import decrypt


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
            is_comic=False,
            is_picture=False,
            is_blog=False,
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
    except Exception:
        log.error("Signup error")
        return False
