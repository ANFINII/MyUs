from django.conf import settings
from django.http import HttpRequest, HttpResponse
from ninja import Router
from ninja.throttling import AnonRateThrottle
from api.modules.logger import log
from api.src.adapter._auth import auth_check
from api.src.types.schema.auth import LoginIn, PasswordChangeIn, PasswordResetEmailIn, PasswordResetIn, PasswordResetVerifyOut, SignupEmailIn, SignupIn, SignupVerifyOut, WithdrawalIn
from api.src.types.schema.common import ErrorOut, ErrorType, SuccessOut
from api.src.usecase.auth import change_password, create_auth_tokens, login_user, password_reset_send_email, password_reset_verify_token, reset_password, signup_send_email, signup_user, signup_verify_token, verify_token, withdraw_user
from api.src.usecase.user import signup_check


class LoginThrottle(AnonRateThrottle):
    scope = "login"


class MailThrottle(AnonRateThrottle):
    scope = "mail"


class AuthAPI:
    """AuthAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def auth(request: HttpRequest):
        log.info("AuthAPI auth")

        ret = auth_check(request)
        if ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        return 200, SuccessOut(message="認証済みです!")

    @staticmethod
    @router.post("refresh", response={200: None, 400: ErrorOut, 500: ErrorOut})
    def refresh(request: HttpRequest, response: HttpResponse):
        log.info("AuthAPI refresh")

        token = request.COOKIES.get("refresh_token")
        if token is None:
            log.warning("No refresh token in cookies")
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Refresh token not found")

        user_id_ret = verify_token(token, "refresh")
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        tokens_ret = create_auth_tokens(user_id)
        if tokens_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        tokens = tokens_ret.ok_value
        if tokens is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        access, _ = tokens
        response.delete_cookie("access_token")
        response.set_cookie("access_token", access, max_age=60 * 60 * 24, httponly=True, secure=settings.SESSION_COOKIE_SECURE, samesite=settings.SESSION_COOKIE_SAMESITE)

        return 200, None

    @staticmethod
    @router.post("/signup/email", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut}, throttle=MailThrottle("5/10m"))
    def signup_email(request: HttpRequest, input: SignupEmailIn):
        log.info("AuthAPI signup_email")

        ret = signup_send_email(input.email)
        if ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        message = ret.ok_value
        if len(message) > 0:
            return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)

        return 200, SuccessOut(message="メールを送信しました!")

    @staticmethod
    @router.get("/signup/verify", response={200: SignupVerifyOut, 400: ErrorOut})
    def signup_verify(request: HttpRequest, token: str):
        log.info("AuthAPI signup_verify")

        email = signup_verify_token(token)
        if email is None:
            return 400, ErrorOut(type=ErrorType.VALIDATION, message="error.linkExpired")

        return 200, SignupVerifyOut(email=email)

    @staticmethod
    @router.post("/signup", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def signup(request: HttpRequest, input: SignupIn):
        log.info("AuthAPI signup", username=input.username)

        token_email = signup_verify_token(input.token)
        if token_email is None:
            log.warning("Signup token invalid")
            return 400, ErrorOut(type=ErrorType.VALIDATION, message="error.linkExpired")

        if token_email != input.email:
            log.warning("Signup email mismatch")
            return 400, ErrorOut(type=ErrorType.VALIDATION, message="error.emailMismatch")

        check_ret = signup_check(input)
        if check_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        message = check_ret.ok_value
        if len(message) > 0:
            log.warning("Signup validation failed", message=message)
            return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)

        ret = signup_user(input)
        if ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="error.signupFailed")

        return 200, SuccessOut(message="アカウント登録が完了しました!")

    @staticmethod
    @router.post("/login", response={200: None, 400: ErrorOut, 500: ErrorOut}, throttle=LoginThrottle("10/m"))
    def login(request: HttpRequest, response: HttpResponse, input: LoginIn):
        log.info("AuthAPI login", username=input.username)

        user_id_ret = login_user(input.username, input.password)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.VALIDATION, message="error.loginFailed")

        tokens_ret = create_auth_tokens(user_id)
        if tokens_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="error.tokenCreateFailed")

        tokens = tokens_ret.ok_value
        if tokens is None:
            return 400, ErrorOut(type=ErrorType.VALIDATION, message="error.loginFailed")

        access, refresh = tokens

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.set_cookie("access_token", access, max_age=60 * 60 * 24, httponly=True, secure=settings.SESSION_COOKIE_SECURE, samesite=settings.SESSION_COOKIE_SAMESITE)
        response.set_cookie("refresh_token", refresh, max_age=60 * 60 * 24 * 30, httponly=True, secure=settings.SESSION_COOKIE_SECURE, samesite=settings.SESSION_COOKIE_SAMESITE)

        return 200, None

    @staticmethod
    @router.post("/logout", response={200: None})
    def logout(request: HttpRequest, response: HttpResponse):
        log.info("AuthAPI logout")

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return 200, None

    @staticmethod
    @router.post("/password/change", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def password_change(request: HttpRequest, response: HttpResponse, input: PasswordChangeIn):
        log.info("AuthAPI password_change")

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        change_ret = change_password(user_id, input)
        if change_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        message = change_ret.ok_value
        if len(message) > 0:
            return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)

        tokens_ret = create_auth_tokens(user_id)
        if tokens_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        tokens = tokens_ret.ok_value
        if tokens is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        access, refresh = tokens
        response.set_cookie("access_token", access, max_age=60 * 60 * 24, httponly=True, secure=settings.SESSION_COOKIE_SECURE, samesite=settings.SESSION_COOKIE_SAMESITE)
        response.set_cookie("refresh_token", refresh, max_age=60 * 60 * 24 * 30, httponly=True, secure=settings.SESSION_COOKIE_SECURE, samesite=settings.SESSION_COOKIE_SAMESITE)

        return 200, SuccessOut(message="パスワードを変更しました!")

    @staticmethod
    @router.post("/password/reset/email", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut}, throttle=MailThrottle("5/10m"))
    def password_reset_email(request: HttpRequest, input: PasswordResetEmailIn):
        log.info("AuthAPI password_reset_email")

        ret = password_reset_send_email(input.email)
        if ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        message = ret.ok_value
        if len(message) > 0:
            return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)

        return 200, SuccessOut(message="メールを送信しました!")

    @staticmethod
    @router.get("/password/reset/verify", response={200: PasswordResetVerifyOut, 400: ErrorOut, 500: ErrorOut})
    def password_reset_verify(request: HttpRequest, token: str):
        log.info("AuthAPI password_reset_verify")

        ret = password_reset_verify_token(token)
        if ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        verified = ret.ok_value
        if verified is None:
            return 400, ErrorOut(type=ErrorType.VALIDATION, message="error.linkExpired")

        _, email = verified
        return 200, PasswordResetVerifyOut(email=email)

    @staticmethod
    @router.post("/password/reset", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def password_reset(request: HttpRequest, input: PasswordResetIn):
        log.info("AuthAPI password_reset")

        ret = reset_password(input)
        if ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        message = ret.ok_value
        if len(message) > 0:
            return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)

        return 200, SuccessOut(message="パスワードをリセットしました!")

    @staticmethod
    @router.post("/withdrawal", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def withdrawal(request: HttpRequest, response: HttpResponse, input: WithdrawalIn):
        log.info("AuthAPI withdrawal")

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        withdraw_ret = withdraw_user(user_id, input)
        if withdraw_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        message = withdraw_ret.ok_value
        if len(message) > 0:
            return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return 200, SuccessOut(message="退会しました!")
