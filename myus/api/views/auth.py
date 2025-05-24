import jwt
import datetime

from django.conf import settings
from django.contrib.auth import authenticate
from django.middleware.csrf import get_token

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView
from rest_framework_simplejwt import views
from rest_framework_simplejwt import exceptions

from api.models import User, Profile
from api.services.user import signup_check
from api.utils.enum.response import ApiResponse
from api.utils.functions.encrypt import encrypt, decrypt
from api.utils.functions.index import message


class AuthAPI(APIView):
    def get(self, request):
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return ApiResponse.UNAUTHORIZED.run()

        user_id = self.get_object(access_token)
        user = User.objects.filter(id=user_id).first()
        if not user.is_active:
            return Response(message(True, "退会済みです!"), status=HTTP_400_BAD_REQUEST)
        return Response(message(False, "認証済みです!"), status=HTTP_200_OK)

    def get_object(self, access_token):
        key = settings.SECRET_KEY
        try:
            payload = jwt.decode(jwt=access_token, key=key, algorithms=["HS256"])
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            return Response(message(True, "認証エラーが発生しました!"), status=HTTP_500_INTERNAL_SERVER_ERROR)
        except jwt.exceptions.DecodeError:
            return Response(message(True, "認証エラーが発生しました!"), status=HTTP_500_INTERNAL_SERVER_ERROR)


class RefreshAPI(views.TokenRefreshView):
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        access = serializer.validated_data["access"]
        response = Response(serializer.validated_data, status=HTTP_200_OK)
        response.delete_cookie("access_token")
        response.set_cookie("access_token", access, max_age=60 * 24 * 24 * 30, httponly=True)
        return response


class SignUpAPI(CreateAPIView):
    def post(self, request):
        data = request.data
        email = data["email"]
        username = data["username"]
        nickname = data["nickname"]
        password1 = data["password1"]

        validation = signup_check(request.data)
        if validation:
            return Response(message(True, validation), status=HTTP_400_BAD_REQUEST)

        birthday = datetime.date(year=int(data["year"]), month=int(data["month"]), day=int(data["day"]))

        try:
            user = User.objects.create_user(email, username, nickname, password1)
            profile = Profile.objects.get(user=user)
            profile.last_name = data["last_name"]
            profile.first_name = data["first_name"]
            profile.gender = data["gender"]
            profile.birthday = birthday.isoformat()
            profile.save()
            return Response(message(False, "アカウント登録が完了しました!"), status=HTTP_201_CREATED)
        except Exception:
            return Response(message(True, "アカウント登録に失敗しました!"), status=HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPI(views.TokenObtainPairView):
    def post(self, request):
        decrypt_data = request.data
        data = {
            "username": decrypt(decrypt_data["username"]),
            "password": decrypt(decrypt_data["password"]),
        }
        username = data["username"]
        password = data["password"]

        user = authenticate(username=username, password=password)
        if not user:
            user = authenticate(email=username, password=password)

        if not user:
            return Response(message(True, "ID又はパスワードが違います!"), status=HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response(message(True, "退会済みのユーザーです!"), status=HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=HTTP_200_OK)
        try:
            response.delete_cookie("access_token")
        except Exception:
            return Response(message(True, "Not Access Token"), status=HTTP_500_INTERNAL_SERVER_ERROR)

        access = serializer.validated_data["access"]
        refresh = serializer.validated_data["refresh"]
        response.set_cookie("access_token", access, max_age=60 * 60 * 24 * 10, httponly=True)
        response.set_cookie("refresh_token", refresh, max_age=60 * 60 * 24 * 30, httponly=True)
        response.data["user"] = {"id": encrypt(str(user.id)), "avatar": user.image(), "nickname": user.nickname, "is_staff": user.is_staff}
        return response


class LogoutAPI(views.TokenObtainPairView):
    def post(self, request):
        response = Response(message(False, "success"), status=HTTP_204_NO_CONTENT)
        try:
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response
        except Exception:
            return Response(message(True, "Exception"), status=HTTP_500_INTERNAL_SERVER_ERROR)
