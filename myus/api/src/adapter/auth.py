from dataclasses import asdict
from datetime import date
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpRequest, HttpResponse
from ninja import Router
from api.modules.logger import log
from api.src.domain.user import UserDomain
from api.src.types.data.setting import ProfileCreateData
from api.src.types.data.user import UserCreateData
from api.src.types.schema.auth import LoginIn, LoginOut, RefreshOut, SignupIn
from api.src.types.schema.common import ErrorOut, MessageOut
from api.src.usecase.user import signup_check
from api.utils.functions.encrypt import decrypt
from api.utils.functions.token import access_token, refresh_token


class AuthAPI:
    """AuthAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: MessageOut, 400: MessageOut, 401: ErrorOut})
    def auth(request: HttpRequest):
        log.info("AuthAPI auth")

        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return 401, ErrorOut(message="Unauthorized")

        key = settings.SECRET_KEY
        try:
            payload = jwt.decode(jwt=access_token, key=key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                return 401, ErrorOut(message="Invalid token")

            user = UserDomain.get(id=user_id)
            if not user:
                return 401, ErrorOut(message="User not found")

            if not user.is_active:
                return 400, MessageOut(error=True, message="退会済みです!")

            return 200, MessageOut(error=False, message="認証済みです!")
        except jwt.ExpiredSignatureError:
            log.warning("Token expired")
            return 401, ErrorOut(message="Token expired")
        except jwt.exceptions.DecodeError:
            log.warning("Token decode error")
            return 401, ErrorOut(message="Invalid token")

    @staticmethod
    @router.post("refresh", response={200: RefreshOut, 401: ErrorOut, 500: MessageOut})
    def refresh(request: HttpRequest, response: HttpResponse):
        log.info("AuthAPI refresh")

        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            log.warning("No refresh token in cookies")
            return 401, ErrorOut(message="Refresh token not found")

        try:
            payload = jwt.decode(
                jwt=refresh_token,
                key=settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            if payload.get("type") != "refresh":
                log.warning("Invalid token type")
                return 401, ErrorOut(message="Invalid token type")

            user_id = payload.get("user_id")
            if not user_id:
                log.warning("No user_id in token")
                return 401, ErrorOut(message="Invalid token")

            user = UserDomain.get(id=user_id)
            if not user:
                log.warning("User not found", user_id=user_id)
                return 401, ErrorOut(message="User not found")

            if not user.is_active:
                log.warning("User is not active", user_id=user_id)
                return 401, ErrorOut(message="User is not active")

            access = access_token(user_id)

        except jwt.ExpiredSignatureError:
            log.warning("Refresh token expired")
            return 401, ErrorOut(message="Refresh token expired")
        except jwt.exceptions.DecodeError:
            log.warning("Token decode error")
            return 401, ErrorOut(message="Invalid token")
        except Exception:
            log.error("Unexpected error during token refresh")
            return 500, MessageOut(error=True, message="トークンリフレッシュに失敗しました!")

        response.delete_cookie("access_token")
        response.set_cookie("access_token", access, max_age=60 * 60 * 24, httponly=True)

        return 200, RefreshOut(access=access)

    @staticmethod
    @router.post("/signup", response={201: MessageOut, 400: MessageOut, 500: MessageOut})
    def signup(request: HttpRequest, input: SignupIn):
        log.info("AuthAPI signup", input=input)

        validation = signup_check(input)
        if validation:
            return 400, MessageOut(error=True, message=validation)

        user_data = UserCreateData(email=input.email, username=input.username, nickname=input.nickname, password=input.password1)
        birthday = date(year=input.year, month=input.month, day=input.day)

        profile_data = ProfileCreateData(last_name=input.last_name, first_name=input.first_name, gender=input.gender, birthday=birthday)

        try:
            user = UserDomain.create(**asdict(user_data))
            UserDomain.update_profile(user, **asdict(profile_data))
            return 201, MessageOut(error=False, message="アカウント登録が完了しました!")
        except Exception:
            log.error("Signup error")
            return 500, MessageOut(error=True, message="アカウント登録に失敗しました!")

    @staticmethod
    @router.post("/login", response={200: LoginOut, 400: MessageOut, 500: MessageOut})
    def login(request: HttpRequest, response: HttpResponse, input: LoginIn):
        log.info("AuthAPI login", username=input.username)

        try:
            username = decrypt(input.username)
            password = decrypt(input.password)
        except Exception:
            log.error("Decrypt error")
            return 500, MessageOut(error=True, message="認証エラーが発生しました!")

        user = authenticate(username=username, password=password)
        if not user:
            user = authenticate(email=username, password=password)

        if not user:
            return 400, MessageOut(error=True, message="ID又はパスワードが違います!")

        if not user.is_active:
            return 400, MessageOut(error=True, message="退会済みのユーザーです!")

        try:
            access = access_token(user.id)
            refresh = refresh_token(user.id)
        except Exception:
            log.error("Token generation error")
            return 500, MessageOut(error=True, message="認証トークンの生成に失敗しました!")

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.set_cookie("access_token", access, max_age=60 * 60 * 24, httponly=True)
        response.set_cookie("refresh_token", refresh, max_age=60 * 60 * 24 * 30, httponly=True)

        return 200, LoginOut(access=access, refresh=refresh)

    @staticmethod
    @router.post("/logout", response={204: None, 500: MessageOut})
    def logout(request: HttpRequest, response: HttpResponse):
        log.info("AuthAPI logout")

        try:
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return 204, None
        except Exception:
            log.error("Logout error")
            return 500, MessageOut(error=True, message="ログアウトに失敗しました!")
