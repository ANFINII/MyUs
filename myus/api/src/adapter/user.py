from ninja import Router

from api.modules.logger import log
from api.src.usecase.follow import get_follows, get_followers, upsert_follow
from api.src.usecase.notification import get_notification, get_content_object
from api.src.usecase.user import get_user, get_search_tags, like_comment, like_media
from api.src.types.data.auth import MessageData
from api.src.types.data.common import ErrorData
from api.src.types.data.follow.index import FollowOutData, FollowUserData
from api.src.types.data.follow.input import FollowInData
from api.src.types.data.notification import NotificationOutData, NotificationItemData, NotificationUserData, NotificationContentData
from api.src.types.data.user import LikeOutData, SearchTagData, UserData, LikeCommentInData, LikeMediaInData
from api.utils.functions.index import create_url


class UserAPI:
    """ユーザーAPI"""

    router = Router()

    @router.get("/me", response={200: UserData, 401: ErrorData})
    def get_user_me(request):
        log.info("UserAPI get_user_me")

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = UserData(
            avatar=create_url(user.image()),
            ulid=str(user.ulid),
            nickname=user.nickname,
            is_active=user.is_active,
            is_staff=user.is_staff,
        )
        return 200, data

    @router.get("/search_tag", response={200: list[SearchTagData], 401: ErrorData})
    def get_search_tag(request):
        log.info("UserAPI search_tag")

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = get_search_tags(user.id)
        return 200, data

    @router.get("/follower", response={200: list[FollowUserData], 401: ErrorData})
    def get_followers(request, search: str = ""):
        log.info("UserAPI get_followers", search=search)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = get_followers(user.id, search, 100)
        return 200, data

    @router.get("/follow", response={200: list[FollowUserData], 401: ErrorData})
    def get_follows(request, search: str = ""):
        log.info("UserAPI get_follows", search=search)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = get_follows(user.id, search, 100)
        return 200, data

    @router.post("/follow/user", response={200: FollowOutData, 400: MessageData, 401: ErrorData, 500: MessageData})
    def follow_user(request, input: FollowInData):
        log.info("UserAPI follow_user", input=input)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = upsert_follow(user, input.ulid, input.is_follow)
        if not data:
            return 400, MessageData(error=True, message="ユーザーが見つかりません!")

        return 200, data

    @router.post("/like/media", response={200: LikeOutData, 400: MessageData, 401: ErrorData, 500: MessageData})
    def post_like_media(request, input: LikeMediaInData):
        log.info("UserAPI like_media", input=input)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = like_media(user, input.media_type, input.ulid)
        if not data:
            return 400, MessageData(error=True, message="メディアが見つかりません!")

        return 200, data

    @router.post("/like/comment", response={200: LikeOutData, 400: MessageData, 401: ErrorData, 404: ErrorData, 500: MessageData})
    def post_like_comment(request, input: LikeCommentInData):
        log.info("UserAPI like_comment", input=input)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = like_comment(user, input.ulid)
        if not data:
            return 400, MessageData(error=True, message="コメントが見つかりません!")

        return 200, data

    @router.get("/notification", response={200: NotificationOutData, 401: ErrorData, 500: MessageData})
    def get_notifications(request):
        log.info("UserAPI get_notifications")

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        notification = get_notification(user)
        data = NotificationOutData(
            count=notification["count"],
            datas=[
                NotificationItemData(
                    id=obj.id,
                    user_from=NotificationUserData(
                        avatar=create_url(obj.user_from.image()),
                        nickname=obj.user_from.nickname,
                    ),
                    user_to=NotificationUserData(
                        avatar=create_url(obj.user_to.image()) if obj.user_to else "",
                        nickname=obj.user_to.nickname if obj.user_to else "",
                    ),
                    type_no=obj.type_no,
                    type_name=obj.type_name,
                    content_object=NotificationContentData(**get_content_object(obj)),
                    is_confirmed=obj.is_confirmed,
                )
                for obj in notification["datas"]
            ],
        )
        return 200, data
