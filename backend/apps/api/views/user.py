from django.contrib.auth import get_user_model

from config.settings.base import DOMAIN_URL
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from apps.myus.modules.filter_data import DeferData
from apps.myus.models import MyPage, Follow, NotificationSetting, SearchTag
from apps.api.services.user import get_user_id
from apps.api.utils.functions.logger import Log


User = get_user_model()


class UserAPI(APIView):
    def get(self, request):
        auth = get_user_id(request)
        if auth.status_code != HTTP_200_OK:
            return Response({'message': auth.data.get('message')}, status=auth.status_code)

        user_id = auth.data['user_id']
        user = User.objects.filter(id=user_id).first()

        data = {
            'avatar': f'{DOMAIN_URL}{user.image()}' if user.image() else '',
            'email': user.email,
            'nickname': user.nickname,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
        }
        return Response(data, status=HTTP_200_OK)


class ProfileAPI(APIView):
    def get(self, request):
        auth = get_user_id(request)
        if auth.status_code != HTTP_200_OK:
            return Response({'message': auth.data.get('message')}, status=auth.status_code)

        user_id = auth.data['user_id']
        user = User.objects.filter(id=user_id).select_related('profile').defer(*DeferData.profile).first()

        data = {
            'avatar': f'{DOMAIN_URL}{user.image()}' if user.image() else '',
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

    def post(self, request):
        auth = get_user_id(request)
        if auth.status_code != HTTP_200_OK:
            return Response({'message': auth.data.get('message')}, status=auth.status_code)

        user_id = auth.data['user_id']
        mypage = MyPage.objects.filter(id=user_id).first()

        data = request.data
        update_fields = ['banner', 'email', 'is_advertise', 'tag_manager_id', 'content']
        for field in update_fields:
            setattr(mypage, field, data.get(field))
        mypage.save()

        return Response({'message': 'success'}, status=HTTP_204_NO_CONTENT)


class FollowAPI(APIView):
    def get(self, request):
        auth = get_user_id(request)
        if auth.status_code != HTTP_200_OK:
            return Response({'message': auth.data.get('message')}, status=auth.status_code)

        user_id = auth.data['user_id']
        follows = Follow.objects.filter(follower=user_id).select_related('following__mypage').order_by('created')[:100]

        data = [{
            'avatar': f'{DOMAIN_URL}{follow.following.avatar.url}',
            'nickname': follow.following.nickname,
            'introduction': follow.following.profile.introduction,
            'follower_count': follow.following.mypage.follower_count,
            'following_count': follow.following.mypage.following_count,
        } for follow in follows]

        return Response(data, status=HTTP_200_OK)


class FollowerAPI(APIView):
    def get(self, request):
        auth = get_user_id(request)
        if auth.status_code != HTTP_200_OK:
            return Response({'message': auth.data.get('message')}, status=auth.status_code)

        user_id = auth.data['user_id']
        follows = Follow.objects.filter(following=user_id).select_related('follower__mypage').order_by('created')[:100]

        data = [{
            'avatar': f'{DOMAIN_URL}{follow.follower.avatar.url}',
            'nickname': follow.follower.nickname,
            'introduction': follow.follower.profile.introduction,
            'follower_count': follow.follower.mypage.follower_count,
            'following_count': follow.follower.mypage.following_count,
        } for follow in follows]

        return Response(data, status=HTTP_200_OK)


class SearchTagAPI(APIView):
    def get(self, request):
        auth = get_user_id(request)
        if auth.status_code != HTTP_200_OK:
            return Response({'message': auth.data.get('message')}, status=auth.status_code)

        user_id = auth.data['user_id']
        search_tags = SearchTag.objects.filter(author=user_id).order_by('sequence')[:20]

        data = [{'sequence': tag.sequence, 'name': tag.name} for tag in search_tags]
        return Response(data, status=HTTP_200_OK)

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
        auth = get_user_id(request)
        if auth.status_code != HTTP_200_OK:
            return Response({'message': auth.data.get('message')}, status=auth.status_code)

        user_id = auth.data['user_id']
        notification_setting = NotificationSetting.objects.filter(user=user_id).first()

        data = request.data
        if notification_setting:
            [setattr(notification_setting, key, value) for key, value in data.items()]
            notification_setting.save()

        return Response({'message': 'success'}, status=HTTP_204_NO_CONTENT)
