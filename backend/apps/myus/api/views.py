from datetime import date

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import JsonResponse
from rest_framework import authentication, permissions, status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView, View
from rest_framework.viewsets import ModelViewSet

from apps.myus.api.serializers import UserSerializer, SignUpSerializer
from apps.myus.modules.validation import has_username, has_email, has_phone, has_postal_code, has_alphabet, has_number
from apps.myus.models import User, Profile, MyPage, SearchTag, HashTag, NotificationSetting
from apps.myus.models import Notification, Follow, Comment, Message, Advertise
from apps.myus.models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo


User = get_user_model()


class SignUpAPIView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request):
        data = request.data

        email = data['email']
        username = data['username']
        nickname = data['nickname']
        password1 = data['password1']
        password2 = data['password2']
        last_name = data['last_name']
        first_name = data['first_name']
        year = data['year']
        month = data['month']
        day = data['day']
        gender = data['gender']

        if has_email(email):
            return Response(
                {'error': 'メールアドレスの形式が違います!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if has_username(username):
            return Response(
                {'error': 'ユーザー名は半角英数字のみ入力できます!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if has_number(last_name):
            return Response(
                {'error': '姓に数字が含まれております!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if has_number(first_name):
            return Response(
                {'error': '名に数字が含まれております!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not has_number(year):
            return Response(
                {'error': '生年月日の年を入力してください!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not has_number(month):
            return Response(
                {'error': '生年月日の月を入力してください!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not has_number(day):
            return Response(
                {'error': '生年月日の日を入力してください!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not has_alphabet(password1) or not has_number(password1):
            return Response(
                {'error': 'パスワードは8文字以上で数字とアルファベットが含まれる必要があります!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if password1 != password2:
            return Response(
                {'error': 'パスワードが一致していません!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'メールアドレスは既に登録されております!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'ユーザー名は既に登録されております!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(nickname=nickname).exists():
            return Response(
                {'error': '投稿者名は既に登録されております!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if year and month and day:
            try:
                birthday = date(year=int(year), month=int(month), day=int(day)).isoformat()
            except ValueError:
                return Response(
                    {'error': f'{year}年{month}月{day}日は存在しない日付です!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        try:
            user = User.objects.create_user(email, username, nickname, password1)
            profile = Profile.objects.filter(user=user).first()
            profile.last_name = last_name
            profile.first_name = first_name
            profile.gender = gender
            profile.birthday = birthday
            profile.save()
            return Response({'succss': 'アカウント登録が完了しました!!'}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(
                {'error': 'アカウント登録に失敗しました!!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginAPIView(APIView):
    pass


class UserView(ListAPIView):
    def get(self, request):
        try:
            user = request.user
            user = UserSerializer(user)
            return Response({'user': user.data}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {'error': 'ユーザーの取得に失敗しました!!'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class Index(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        nicknames = [user.nickname for user in User.objects.all()]
        return Response(nicknames)

    def post(self, request):
        # 普通こんなことはしないが..
        users = [User(username=username) for username in request.POST.getlist('username')]
        User.objects.bulk_create(users)
        return Response({'succeeded': True})
