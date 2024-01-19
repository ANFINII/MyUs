from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.myus.modules.filter_data import DeferData
from apps.myus.models import NotificationSetting
from apps.api.services.user import get_user_id


User = get_user_model()


class UserAPI(APIView):
    def get(self, request):
        user_id = get_user_id(request)
        user = User.objects.filter(id=user_id).defer(*DeferData.user).first()
        data = {'avatar': user.image(), 'nickname': user.nickname, 'is_staff': user.is_staff}
        return Response(data, status=HTTP_200_OK)


class ProfileAPI(APIView):
    def get(self, request):
        user_id = get_user_id(request)
        user = User.objects.filter(id=user_id).select_related('profile').defer(*DeferData.profile).first()

        data = {
            'avatar': user.image(),
            'email': user.email,
            'username': user.username,
            'nickname': user.nickname,
            'fullname': user.fullname(),
            'lastname': user.profile.last_name,
            'firstname': user.profile.first_name,
            'year': user.year(),
            'month': user.month(),
            'day': user.day(),
            'age': user.age(),
            'gender': user.gender(),
            'phone': user.profile.phone,
            'country_code': user.profile.country_code,
            'postal_code': user.profile.postal_code,
            'city': user.profile.city,
            'address': user.profile.address,
            'building': user.profile.building,
            'introduction': user.profile.introduction,
        }
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        pass


class MyPageAPI(APIView):
    def get(self, request):
        user_id = get_user_id(request)
        user = User.objects.filter(id=user_id).select_related('mypage').defer(*DeferData.mypage).first()

        data = {
            'banner': user.banner(),
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

    def post(self, request):
        pass


class NotificationAPI(APIView):
    def get(self, request):
        user_id = get_user_id(request)
        notification_setting = NotificationSetting.objects.filter(id=user_id).first()

        data = {
            'is_video': notification_setting.is_video,
            'is_music': notification_setting.is_music,
            'is_comic': notification_setting.is_comic,
            'is_picture': notification_setting.is_picture,
            'is_blog': notification_setting.is_blog,
            'is_chat': notification_setting.is_chat,
            'is_follow': notification_setting.is_follow,
            'is_reply': notification_setting.is_reply,
            'is_like': notification_setting.is_like,
            'is_views': notification_setting.is_views,
        }
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        pass
