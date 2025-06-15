from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from api.models import User, Follow, SearchTag
from app.modules.follow import follow_update_data
from api.services.notification import get_notification, get_content_object
from api.services.user import get_user, get_follows, get_followers
from api.types.data.user import UserData
from api.utils.enum.response import ApiResponse
from api.utils.functions.index import create_url
from api.utils.functions.response import DataResponse
from api.utils.functions.user import get_notification_user


class UserAPI(APIView):
    def get(self, request) -> DataResponse:
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        data = UserData(
            avatar=create_url(user.image()),
            email=user.email,
            nickname=user.nickname,
            is_active=user.is_active,
            is_staff=user.is_staff,
        )
        return DataResponse(data, HTTP_200_OK)


class SearchTagAPI(APIView):
    def get(self, request) -> DataResponse:
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        search_tags = SearchTag.objects.filter(author=user).order_by("sequence")[:20]

        data = [{"sequence": tag.sequence, "name": tag.name} for tag in search_tags]
        return DataResponse(data, HTTP_200_OK)


class FollowAPI(APIView):
    def get(self, request) -> DataResponse:
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        search = request.query_params.get("search")
        data = get_follows(100, user, search)
        return DataResponse(data, HTTP_200_OK)

    def post(self, request) -> DataResponse:
        user = get_user(request)
        data = request.data
        nickname = data.get("nickname")

        followwe = user
        following = User.objects.get(nickname=nickname)
        follow = Follow.objects.filter(follower=followwe, following=following).first()
        follow_data = follow_update_data(followwe, following, follow)
        data = {
            "is_follow": follow_data["is_follow"],
            "follower_count": follow_data["follower_count"],
        }
        return DataResponse(data, status=HTTP_201_CREATED)


class FollowerAPI(APIView):
    def get(self, request) -> DataResponse:
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        search = request.query_params.get("search")
        data = get_followers(100, user, search)
        return DataResponse(data, HTTP_200_OK)


class NotificationAPI(APIView):
    def get(self, request) -> DataResponse:
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

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
