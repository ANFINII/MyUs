from config.settings.base import DOMAIN_URL
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.myus.models import SearchTag
from apps.api.services.notification import get_notification, get_content_object
from apps.api.services.user import get_user, get_follows, get_followers
from apps.api.utils.enum.response import ApiResponse
from apps.api.utils.functions.user import get_notification_user


class UserAPI(APIView):
    def get(self, request):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        data = {
            'avatar': f'{DOMAIN_URL}{user.image()}' if user.image() else '',
            'email': user.email,
            'nickname': user.nickname,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
        }
        return Response(data, status=HTTP_200_OK)


class SearchTagAPI(APIView):
    def get(self, request):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        search_tags = SearchTag.objects.filter(author=user).order_by('sequence')[:20]

        data = [{'sequence': tag.sequence, 'name': tag.name} for tag in search_tags]
        return Response(data, status=HTTP_200_OK)


class FollowAPI(APIView):
    def get(self, request):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        search = request.query_params.get('search')
        data = get_follows(100, user, search)
        return Response(data, status=HTTP_200_OK)


class FollowerAPI(APIView):
    def get(self, request):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        search = request.query_params.get('search')
        data = get_followers(100, user, search)
        return Response(data, status=HTTP_200_OK)


class NotificationAPI(APIView):
    def get(self, request):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        notification = get_notification(user)
        data = {
            'count': notification['count'],
            'datas': [
                {
                    'id': obj.id,
                    'user_from': get_notification_user(obj.user_from),
                    'user_to': get_notification_user(obj.user_to),
                    'type_no': obj.type_no,
                    'type_name': obj.type_name,
                    'content_object': get_content_object(obj),
                    'is_confirmed': obj.is_confirmed,
                } for obj in notification['datas']
            ],
        }
        return Response(data, status=HTTP_200_OK)
