import jwt
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from ninja import Router
from api.modules.logger import log
from api.src.types.schema.auth import LoginIn, LoginOut, RefreshOut, SignupIn
from api.src.types.schema.common import ErrorOut
from api.src.usecase.auth import login_user, signup_user, verify_user
from api.src.usecase.user import signup_check
from api.utils.functions.token import access_token, refresh_token


class AuthAPI:
    """AuthAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def auth(request: HttpRequest):
        log.info("AuthAPI auth")

        token = request.COOKIES.get("access_token")
        if not token:
            return 401, ErrorOut(message="Unauthorized")

        key = settings.SECRET_KEY
        try:
            payload = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                return 401, ErrorOut(message="Invalid token")

            if not verify_user(user_id):
                return 401, ErrorOut(message="Unauthorized")

            return 200, ErrorOut(message="認証済みです!")
        except jwt.ExpiredSignatureError:
            log.warning("Token expired")
            return 401, ErrorOut(message="Token expired")
        except jwt.exceptions.DecodeError:
            log.warning("Token decode error")
            return 401, ErrorOut(message="Invalid token")

    @staticmethod
    @router.post("refresh", response={200: RefreshOut, 401: ErrorOut, 500: ErrorOut})
    def refresh(request: HttpRequest, response: HttpResponse):
        log.info("AuthAPI refresh")

        token = request.COOKIES.get("refresh_token")
        if not token:
            log.warning("No refresh token in cookies")
            return 401, ErrorOut(message="Refresh token not found")

        try:
            payload = jwt.decode(
                jwt=token,
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

            if not verify_user(user_id):
                log.warning("User verification failed", user_id=user_id)
                return 401, ErrorOut(message="Unauthorized")

            access = access_token(user_id)

        except jwt.ExpiredSignatureError:
            log.warning("Refresh token expired")
            return 401, ErrorOut(message="Refresh token expired")
        except jwt.exceptions.DecodeError:
            log.warning("Token decode error")
            return 401, ErrorOut(message="Invalid token")
        except Exception:
            log.error("Unexpected error during token refresh")
            return 500, ErrorOut(message="トークンリフレッシュに失敗しました!")

        response.delete_cookie("access_token")
        response.set_cookie("access_token", access, max_age=60 * 60 * 24, httponly=True)

        return 200, RefreshOut(access=access)

    @staticmethod
    @router.post("/signup", response={201: ErrorOut, 400: ErrorOut, 500: ErrorOut})
    def signup(request: HttpRequest, input: SignupIn):
        log.info("AuthAPI signup", input=input)

        validation = signup_check(input)
        if validation:
            return 400, ErrorOut(message=validation)

        if not signup_user(input):
            return 500, ErrorOut(message="アカウント登録に失敗しました!")

        return 201, ErrorOut(message="アカウント登録が完了しました!")

    @staticmethod
    @router.post("/login", response={200: LoginOut, 400: ErrorOut, 500: ErrorOut})
    def login(request: HttpRequest, response: HttpResponse, input: LoginIn):
        log.info("AuthAPI login", username=input.username)

        user_id = login_user(input.username, input.password)
        if user_id is None:
            return 400, ErrorOut(message="ID又はパスワードが違います!")

        try:
            access = access_token(user_id)
            refresh = refresh_token(user_id)
        except Exception:
            log.error("Token generation error")
            return 500, ErrorOut(message="認証トークンの生成に失敗しました!")

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.set_cookie("access_token", access, max_age=60 * 60 * 24, httponly=True)
        response.set_cookie("refresh_token", refresh, max_age=60 * 60 * 24 * 30, httponly=True)

        return 200, LoginOut(access=access, refresh=refresh)

    @staticmethod
    @router.post("/logout", response={204: None, 500: ErrorOut})
    def logout(request: HttpRequest, response: HttpResponse):
        log.info("AuthAPI logout")

        try:
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return 204, None
        except Exception:
            log.error("Logout error")
            return 500, ErrorOut(message="ログアウトに失敗しました!")
