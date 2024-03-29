from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from apps.myus.modules.filter_data import DeferData
from apps.myus.models import NotificationSetting
from apps.api.services.user import get_user_id
from apps.api.utils.functions.logger import Log


User = get_user_model()


class ProfileAPI(APIView):
    def get(self, request):
        auth = get_user_id(request)
        if auth.status_code != HTTP_200_OK:
            return Response({'message': auth.data.get('message')}, status=auth.status_code)

        user_id = auth.data['user_id']
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
            'street': user.profile.street,
            'building': user.profile.building,
            'introduction': user.profile.introduction,
        }
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        data = request.data
        Log.info('ProfileAPI', 'post', data)
        return Response({'message': '保存しました!'}, status=HTTP_204_NO_CONTENT)



class MyPageAPI(APIView):
    def get(self, request):
        auth = get_user_id(request)
        if auth.status_code != HTTP_200_OK:
            return Response({'message': auth.data.get('message')}, status=auth.status_code)

        user_id = auth.data['user_id']
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
        auth = get_user_id(request)
        if auth.status_code != HTTP_200_OK:
            return Response({'message': auth.data.get('message')}, status=auth.status_code)

        user_id = auth.data['user_id']
        notification_setting = NotificationSetting.objects.filter(user=user_id).first()

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
