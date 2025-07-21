from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from api.models import User, Follow, SearchTag
from api.domain.follow import FollowDomain
from api.services.notification import get_notification, get_content_object
from api.services.user import get_user
from api.types.data.user import UserData
from api.utils.decorators.auth import auth_user
from api.utils.functions.index import create_url
from api.utils.functions.response import DataResponse
from api.utils.functions.user import get_notification_user


class UserAPI(APIView):
    @auth_user
    def get(self, request) -> DataResponse:
        user = get_user(request)
        data = UserData(
            avatar=create_url(user.image()),
            email=user.email,
            nickname=user.nickname,
            is_active=user.is_active,
            is_staff=user.is_staff,
        )
        return DataResponse(data, HTTP_200_OK)


class SearchTagAPI(APIView):
    @auth_user
    def get(self, request) -> DataResponse:
        user = get_user(request)
        search_tags = SearchTag.objects.filter(author=user).order_by("sequence")[:20]

        data = [{"sequence": tag.sequence, "name": tag.name} for tag in search_tags]
        return DataResponse(data, HTTP_200_OK)


class FollowAPI(APIView):
    @auth_user
    def get(self, request) -> DataResponse:
        user = get_user(request)
        search = request.query_params.get("search")
        data = FollowDomain.get_follows(user.id, search, 100)
        return DataResponse(data, HTTP_200_OK)

    @auth_user
    def post(self, request) -> DataResponse:
        user = get_user(request)
        data = request.data
        nickname = data.get("nickname")

        following = User.objects.get(nickname=nickname)
        data = FollowDomain.create(user.id, following.id)
        return DataResponse(data, status=HTTP_201_CREATED)

    @auth_user
    def delete(self, request) -> DataResponse:
        user = get_user(request)
        data = request.data
        nickname = data.get("nickname")
        FollowDomain.delete(user.id, nickname)
        return DataResponse(None, status=HTTP_204_NO_CONTENT)


class FollowerAPI(APIView):
    @auth_user
    def get(self, request) -> DataResponse:
        user = get_user(request)
        search = request.query_params.get("search")
        data = FollowDomain.get_followers(user.id, search, 100)
        return DataResponse(data, HTTP_200_OK)


class NotificationAPI(APIView):
    @auth_user
    def get(self, request) -> DataResponse:
        user = get_user(request)
        notification = get_notification(user)

        data = {
            "count": notification["count"],
            "datas": [{
                "id": obj.id,
                "user_from": get_notification_user(obj.user_from),
                "user_to": get_notification_user(obj.user_to),
                "type_no": obj.type_no,
                "type_name": obj.type_name,
                "content_object": get_content_object(obj),
                "is_confirmed": obj.is_confirmed,
            } for obj in notification["datas"]],
        }
        return DataResponse(data, HTTP_200_OK)
