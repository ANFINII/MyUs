from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from api.models import SearchTag
from api.domain.user import UserDomain
from api.services.follow import get_follows, get_followers, upsert_follow
from api.services.notification import get_notification, get_content_object
from api.services.user import get_user
from api.types.data.user import LikeOutData, UserData
from api.utils.constant import media_models
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
            ulid=user.ulid,
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
        data = get_follows(user.id, search, 100)
        return DataResponse(data, HTTP_200_OK)

    @auth_user
    def post(self, request) -> DataResponse:
        user = get_user(request)
        data = request.data
        ulid = data.get("ulid")
        is_follow = data.get("is_follow")
        following = UserDomain.get(ulid=ulid)
        data = upsert_follow(user, following, is_follow)
        return DataResponse(data, status=HTTP_201_CREATED)


class FollowerAPI(APIView):
    @auth_user
    def get(self, request) -> DataResponse:
        user = get_user(request)
        search = request.query_params.get("search")
        data = get_followers(user.id, search, 100)
        return DataResponse(data, HTTP_200_OK)


class LikeMediaAPI(APIView):
    @auth_user
    def post(self, request) -> DataResponse:
        user = get_user(request)
        data = request.data
        obj_id = data['id']
        media_type = data['media_type']

        model = media_models.get(media_type)
        obj = model.objects.get(id=obj_id)
        is_liked = obj.like.filter(id=user.id).exists()

        if is_liked:
            obj.like.remove(user)
            is_like = False
        else:
            obj.like.add(user)
            is_like = True

        data = LikeOutData(is_like=is_like, like_count=obj.total_like())

        return DataResponse(data, status=HTTP_200_OK)


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
