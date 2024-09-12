from config.settings.base import DOMAIN_URL
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.myus.models import SearchTag
from apps.api.services.user import get_user
from apps.api.utils.functions.response import ApiResponse
from apps.api.services.user import get_follows, get_followers


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
