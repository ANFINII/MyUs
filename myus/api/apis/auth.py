import datetime
import jwt

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse
from ninja import Router

from api.models import Profile, User
from api.modules.logger import log
from api.services.user import signup_check
from api.types.data.auth import LoginDataIn, LoginOutData, MessageData, RefreshOutData, SignUpDataIn, UserLoginData
from api.types.data.common import ErrorData
from api.utils.functions.encrypt import decrypt
from api.utils.functions.token import access_token, refresh_token


class AuthAPI:
    """AuthAPI"""

    router = Router()

    @router.get("", response={200: MessageData, 401: ErrorData})
    def auth(request):
        """認証状態確認"""
        log.info("AuthAPI auth")

        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return 401, ErrorData(message="Unauthorized")

        key = settings.SECRET_KEY
        try:
            payload = jwt.decode(jwt=access_token, key=key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                return 401, ErrorData(message="Invalid token")

            user = User.objects.filter(id=user_id).first()
            if not user:
                return 401, ErrorData(message="User not found")

            if not user.is_active:
                return 400, MessageData(error=True, message="退会済みです!")

            return 200, MessageData(error=False, message="認証済みです!")
        except jwt.ExpiredSignatureError:
            log.warning("Token expired")
            return 401, ErrorData(message="Token expired")
        except jwt.exceptions.DecodeError:
            log.warning("Token decode error")
            return 401, ErrorData(message="Invalid token")

    @router.post("refresh", response={200: RefreshOutData, 401: ErrorData, 500: MessageData})
    def refresh(request, response: HttpResponse):
        """トークンリフレッシュ"""
        log.info("AuthAPI refresh")

        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            log.warning("No refresh token in cookies")
            return 401, ErrorData(message="Refresh token not found")

        try:
            payload = jwt.decode(
                jwt=refresh_token,
                key=settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            if payload.get("type") != "refresh":
                log.warning("Invalid token type")
                return 401, ErrorData(message="Invalid token type")

            user_id = payload.get("user_id")
            if not user_id:
                log.warning("No user_id in token")
                return 401, ErrorData(message="Invalid token")

            user = User.objects.filter(id=user_id).first()
            if not user:
                log.warning("User not found", user_id=user_id)
                return 401, ErrorData(message="User not found")

            if not user.is_active:
                log.warning("User is not active", user_id=user_id)
                return 401, ErrorData(message="User is not active")

            access = access_token(user_id)

        except jwt.ExpiredSignatureError:
            log.warning("Refresh token expired")
            return 401, ErrorData(message="Refresh token expired")
        except jwt.exceptions.DecodeError:
            log.warning("Token decode error")
            return 401, ErrorData(message="Invalid token")
        except Exception as e:
            log.error("Unexpected error during token refresh", exc=e)
            return 500, MessageData(error=True, message="トークンリフレッシュに失敗しました!")

        response.delete_cookie("access_token")
        response.set_cookie("access_token", access, max_age=60 * 60 * 24, httponly=True)

        log.info("Token refreshed successfully", user_id=user_id)
        return 200, RefreshOutData(access=access)

    @router.post("/signup", response={201: MessageData, 400: MessageData, 500: MessageData})
    def signup(request, input: SignUpDataIn):
        """サインアップ"""
        log.info("AuthAPI signup", email=input.email, username=input.username)

        validation = signup_check(input.__dict__)
        if validation:
            return 400, MessageData(error=True, message=validation)

        birthday = datetime.date(year=input.year, month=input.month, day=input.day)

        try:
            user = User.objects.create_user(input.email, input.username, input.nickname, input.password1)
            profile = Profile.objects.get(user=user)
            profile.last_name = input.last_name
            profile.first_name = input.first_name
            profile.gender = input.gender
            profile.birthday = birthday.isoformat()
            profile.save()
            log.info("User created", user_id=user.id, username=user.username)
            return 201, MessageData(error=False, message="アカウント登録が完了しました!")
        except Exception as e:
            log.error("Signup error", exc=e)
            return 500, MessageData(error=True, message="アカウント登録に失敗しました!")

    @router.post("/login", response={200: LoginOutData, 400: MessageData, 500: MessageData})
    def login(request, response: HttpResponse, input: LoginDataIn):
        """ログイン"""
        log.info("AuthAPI login", username=input.username)

        try:
            username = decrypt(input.username)
            password = decrypt(input.password)
        except Exception as e:
            log.error("Decrypt error", exc=e)
            return 500, MessageData(error=True, message="認証エラーが発生しました!")

        user = authenticate(username=username, password=password)
        if not user:
            user = authenticate(email=username, password=password)

        if not user:
            return 400, MessageData(error=True, message="ID又はパスワードが違います!")

        if not user.is_active:
            return 400, MessageData(error=True, message="退会済みのユーザーです!")

        try:
            access = access_token(user.id)
            refresh = refresh_token(user.id)
        except Exception as e:
            log.error("Token generation error", exc=e)
            return 500, MessageData(error=True, message="認証トークンの生成に失敗しました!")

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.set_cookie("access_token", access, max_age=60 * 60 * 24, httponly=True)
        response.set_cookie("refresh_token", refresh, max_age=60 * 60 * 24 * 30, httponly=True)

        user = UserLoginData(avatar=user.image(), ulid=str(user.ulid), nickname=user.nickname, is_staff=user.is_staff)
        log.info("User login success", user=user)

        return 200, LoginOutData(access=access, refresh=refresh, user=user)

    @router.post("/logout", response={200: MessageData, 500: MessageData})
    def logout(request, response: HttpResponse):
        """ログアウト"""
        log.info("AuthAPI logout")

        try:
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return 200, MessageData(error=False, message="ログアウトしました!")
        except Exception as e:
            log.error("Logout error", exc=e)
            return 500, MessageData(error=True, message="ログアウトに失敗しました!")
