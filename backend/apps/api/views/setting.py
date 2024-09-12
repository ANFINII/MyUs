import datetime

from config.settings.base import DOMAIN_URL
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.myus.models import User, Profile, MyPage, UserNotification
from apps.myus.modules.filter_data import DeferData
from apps.myus.modules.validation import has_email
from apps.api.services.user import get_user, profile_check
from apps.api.utils.functions.index import message
from apps.api.utils.functions.logger import Log
from apps.api.utils.functions.response import ApiResponse


class SettingProfileAPI(APIView):
    def get(self, request):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        user = User.objects.filter(id=user.id).select_related('profile').defer(*DeferData.profile).first()

        data = {
            'avatar': f'{DOMAIN_URL}{user.image()}' if user.image() else '',
            'email': user.email,
            'username': user.username,
            'nickname': user.nickname,
            'full_name': user.full_name(),
            'last_name': user.profile.last_name,
            'first_name': user.profile.first_name,
            'year': user.year(),
            'month': user.month(),
            'day': user.day(),
            'age': user.age(),
            'gender': user.gender(),
            'phone': user.profile.phone,
            'country_code': user.profile.country_code,
            'postal_code': user.profile.postal_code,
            'prefecture': user.profile.prefecture,
            'city': user.profile.city,
            'street': user.profile.street,
            'introduction': user.profile.introduction,
        }
        return Response(data, status=HTTP_200_OK)

    def put(self, request):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        profile = Profile.objects.filter(id=user.id).first()
        data = request.data
        avatar = data.get('avatar')

        validation = profile_check(request.data)
        if validation:
            return Response(message(True, validation), status=HTTP_400_BAD_REQUEST)

        user_fields = ['email', 'username', 'nickname', 'content']
        [setattr(user, field, data.get(field)) for field in user_fields]
        user.avatar = avatar if avatar else user.avatar

        profile_fields = ('last_name', 'first_name', 'gender', 'phone', 'postal_code', 'prefecture', 'city', 'street', 'introduction')
        [setattr(profile, field, data.get(field)) for field in profile_fields]
        birthday = datetime.date(year=int(data['year']), month=int(data['month']), day=int(data['day']))
        profile.birthday = birthday.isoformat()

        try:
            user.save()
            profile.save()
        except Exception:
            return Response(message(True, 'ユーザー名またはメールアドレス、投稿者名は既に登録済みです!'), status=HTTP_400_BAD_REQUEST)

        Log.info('ProfileAPI', 'put', data)
        return Response(message(False, '保存しました!'), status=HTTP_204_NO_CONTENT)


class SettingMyPageAPI(APIView):
    def get(self, request):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        user = User.objects.filter(id=user.id).select_related('mypage').defer(*DeferData.mypage).first()

        data = {
            'banner': f'{DOMAIN_URL}{user.banner()}' if user.banner() else '',
            'nickname': user.nickname,
            'email': user.mypage.email,
            'content': user.mypage.content,
            'follower_count': user.mypage.follower_count,
            'following_count': user.mypage.following_count,
            'tag_manager_id': user.mypage.tag_manager_id,
            'plan': user.plan(),
            'plan_start_date': user.plan_start_date(),
            'plan_end_date': user.plan_end_date(),
            'is_advertise': user.mypage.is_advertise,
        }
        return Response(data, status=HTTP_200_OK)

    def put(self, request):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        mypage = MyPage.objects.filter(id=user.id).first()
        data = request.data
        banner = data.get('banner')

        if has_email(data['email']):
            return Response(message(True, 'メールアドレスの形式が違います!'), status=HTTP_400_BAD_REQUEST)

        update_fields = ['email', 'tag_manager_id', 'content']
        [setattr(mypage, field, data.get(field)) for field in update_fields]
        mypage.banner = banner if banner else mypage.banner
        mypage.is_advertise = data['is_advertise'] == 'true'

        try:
            mypage.save()
        except Exception:
            return Response(message(True, 'メールアドレスが既に登録済みです!'), status=HTTP_400_BAD_REQUEST)

        Log.info('MyPageAPI', 'put', data)
        return Response(message(False, 'success'), status=HTTP_204_NO_CONTENT)


class SettingNotificationAPI(APIView):
    def get(self, request):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        user_notification = UserNotification.objects.filter(user=user).first()

        data = {
            'is_video': user_notification.is_video,
            'is_music': user_notification.is_music,
            'is_comic': user_notification.is_comic,
            'is_picture': user_notification.is_picture,
            'is_blog': user_notification.is_blog,
            'is_chat': user_notification.is_chat,
            'is_follow': user_notification.is_follow,
            'is_reply': user_notification.is_reply,
            'is_like': user_notification.is_like,
            'is_views': user_notification.is_views,
        }
        return Response(data, status=HTTP_200_OK)

    def put(self, request):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        user_notification = UserNotification.objects.filter(user=user).first()

        data = request.data
        [setattr(user_notification, key, value) for key, value in data.items()]

        try:
            user_notification.save()
        except Exception:
            return Response(message(True, 'メールアドレスが既に登録済みです!'), status=HTTP_400_BAD_REQUEST)

        return Response(message(False, 'success'), status=HTTP_204_NO_CONTENT)
