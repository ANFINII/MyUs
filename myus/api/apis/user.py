from ninja import Router

from api.domain.comment import CommentDomain
from api.domain.user import UserDomain
from api.models import SearchTag
from api.modules.logger import log
from api.services.follow import get_follows, get_followers, upsert_follow
from api.services.notification import get_notification, get_content_object
from api.services.user import get_user
from api.types.data.auth import MessageData
from api.types.data.common import ErrorData
from api.types.data.follow import FollowOutData, FollowUserData, FollowInData, SearchTagData
from api.types.data.notification import NotificationOutData, NotificationItemData, NotificationUserData, NotificationContentData
from api.types.data.user import LikeOutData, UserData, LikeCommentInData, LikeMediaInData
from api.utils.constant import media_models
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

        search_tags = SearchTag.objects.filter(author=user).order_by("sequence")[:20]
        data = [SearchTagData(sequence=tag.sequence, name=tag.name) for tag in search_tags]
        log.info("Search tags retrieved", user_id=user.id, count=len(data))
        return 200, data

    @router.get("/follow", response={200: list[FollowUserData], 401: ErrorData})
    def get_follows(request, search: str = None):
        log.info("UserAPI get_follow_list", search=search)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = get_follows(user.id, search, 100)
        return 200, data

    @router.post("/follow", response={200: FollowOutData, 400: MessageData, 401: ErrorData, 500: MessageData})
    def post_follow_user(request, input: FollowInData):
        log.info("UserAPI follow_user", ulid=input.ulid, is_follow=input.is_follow)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        following = UserDomain.get(ulid=input.ulid)
        if not following:
            return 400, MessageData(error=True, message="ユーザーが見つかりません!")

        try:
            data = upsert_follow(user, following, input.is_follow)
            return 200, data
        except Exception:
            log.error("Follow error")
            return 500, MessageData(error=True, message="フォロー処理に失敗しました!")

    @router.get("/follower", response={200: list[FollowUserData], 401: ErrorData})
    def get_followers(request, search: str = None):
        log.info("UserAPI get_follower_list", search=search)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = get_followers(user.id, search, 100)
        return 200, data

    @router.post("/like/media", response={200: LikeOutData, 400: MessageData, 401: ErrorData, 500: MessageData})
    def post_like_media(request, input: LikeMediaInData):
        log.info("UserAPI like_media", obj_id=input.id, media_type=input.media_type)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        model = media_models.get(input.media_type)
        if not model:
            return 400, MessageData(error=True, message="無効なメディアタイプです!")

        try:
            obj = model.objects.get(id=input.id)
        except model.DoesNotExist:
            return 400, MessageData(error=True, message="メディアが見つかりません!")

        try:
            is_liked = obj.like.filter(id=user.id).exists()
            if is_liked:
                obj.like.remove(user)
                is_like = False
            else:
                obj.like.add(user)
                is_like = True

            data = LikeOutData(is_like=is_like, like_count=obj.total_like())
            return 200, data
        except Exception:
            log.error("Like media error")
            return 500, MessageData(error=True, message="いいね処理に失敗しました!")

    @router.post("/like/comment", response={200: LikeOutData, 400: MessageData, 401: ErrorData, 404: ErrorData, 500: MessageData})
    def post_like_comment(request, input: LikeCommentInData):
        log.info("UserAPI like_comment", obj_id=input.id)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        obj = CommentDomain.get(input.id)
        if not obj:
            return 404, ErrorData(message="コメントが見つかりません!")

        try:
            is_liked = obj.like.filter(id=user.id).exists()
            if is_liked:
                obj.like.remove(user)
                is_like = False
            else:
                obj.like.add(user)
                is_like = True

            data = LikeOutData(is_like=is_like, like_count=obj.total_like())
            return 200, data
        except Exception:
            log.error("Like comment error")
            return 500, MessageData(error=True, message="いいね処理に失敗しました!")

    @router.get("/notification", response={200: NotificationOutData, 401: ErrorData, 500: MessageData})
    def get_notifications(request):
        log.info("UserAPI get_notifications")

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        try:
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
        except Exception:
            log.error("Get notification error")
            return 500, MessageData(error=True, message="通知取得に失敗しました!")
