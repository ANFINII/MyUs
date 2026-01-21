from django.http import HttpRequest
from ninja import Router

from api.modules.logger import log
from api.src.types.schema.channel import ChannelOut
from api.src.types.schema.common import ErrorOut, MessageOut
from api.src.types.schema.follow import FollowIn, FollowOut, FollowUserOut
from api.src.types.schema.notification import NotificationContentOut, NotificationItemOut, NotificationOut, NotificationUserOut
from api.src.types.schema.user import LikeCommentIn, LikeMediaIn, LikeOut, SearchTagOut, UserOut
from api.src.usecase.channel import get_user_channels
from api.src.usecase.follow import get_follows, get_followers, upsert_follow
from api.src.usecase.notification import get_notification, get_content_object
from api.src.usecase.user import get_user, get_search_tags, like_comment, like_media
from api.utils.functions.index import create_url


class UserAPI:
    """ユーザーAPI"""

    router = Router()

    @staticmethod
    @router.get("/me", response={200: UserOut, 401: ErrorOut})
    def get_user_me(request: HttpRequest):
        log.info("UserAPI get_user_me")

        user = get_user(request)
        if not user:
            return 401, ErrorOut(message="Unauthorized")

        data = UserOut(
            avatar=create_url(user.image()),
            ulid=str(user.ulid),
            nickname=user.nickname,
            is_active=user.is_active,
            is_staff=user.is_staff,
        )

        return 200, data

    @staticmethod
    @router.get("/search_tag", response={200: list[SearchTagOut], 401: ErrorOut})
    def get_search_tag(request: HttpRequest):
        log.info("UserAPI search_tag")

        user = get_user(request)
        if not user:
            return 401, ErrorOut(message="Unauthorized")

        tags = get_search_tags(user.id)
        data = [SearchTagOut(sequence=x.sequence, name=x.name) for x in tags]
        return 200, data

    @staticmethod
    @router.get("/follower", response={200: list[FollowUserOut], 401: ErrorOut})
    def get_followers(request: HttpRequest, search: str = ""):
        log.info("UserAPI get_followers", search=search)

        user = get_user(request)
        if not user:
            return 401, ErrorOut(message="Unauthorized")

        followers = get_followers(user.id, search, 100)
        data = [
            FollowUserOut(
                avatar=x.avatar,
                nickname=x.nickname,
                introduction=x.introduction,
                follower_count=x.follower_count,
                following_count=x.following_count,
            )
            for x in followers
        ]

        return 200, data

    @staticmethod
    @router.get("/follow", response={200: list[FollowUserOut], 401: ErrorOut})
    def get_follows(request: HttpRequest, search: str = ""):
        log.info("UserAPI get_follows", search=search)

        user = get_user(request)
        if not user:
            return 401, ErrorOut(message="Unauthorized")

        follows = get_follows(user.id, search, 100)
        data = [
            FollowUserOut(
                avatar=x.avatar,
                nickname=x.nickname,
                introduction=x.introduction,
                follower_count=x.follower_count,
                following_count=x.following_count,
            )
            for x in follows
        ]

        return 200, data

    @staticmethod
    @router.post("/follow/user", response={200: FollowOut, 400: MessageOut, 401: ErrorOut, 500: MessageOut})
    def follow_user(request: HttpRequest, input: FollowIn):
        log.info("UserAPI follow_user", input=input)

        user = get_user(request)
        if not user:
            return 401, ErrorOut(message="Unauthorized")

        follow = upsert_follow(user, input.ulid, input.is_follow)
        if not follow:
            return 400, MessageOut(error=True, message="ユーザーが見つかりません!")

        data = FollowOut(is_follow=follow.is_follow, follower_count=follow.follower_count)
        return 200, data

    @staticmethod
    @router.post("/like/media", response={200: LikeOut, 400: MessageOut, 401: ErrorOut, 500: MessageOut})
    def post_like_media(request: HttpRequest, input: LikeMediaIn):
        log.info("UserAPI like_media", input=input)

        user = get_user(request)
        if not user:
            return 401, ErrorOut(message="Unauthorized")

        like = like_media(user, input.media_type, input.ulid)
        if not like:
            return 400, MessageOut(error=True, message="メディアが見つかりません!")

        data = LikeOut(is_like=like.is_like, like_count=like.like_count)
        return 200, data

    @staticmethod
    @router.post("/like/comment", response={200: LikeOut, 400: MessageOut, 401: ErrorOut, 404: ErrorOut, 500: MessageOut})
    def post_like_comment(request: HttpRequest, input: LikeCommentIn):
        log.info("UserAPI like_comment", input=input)

        user = get_user(request)
        if not user:
            return 401, ErrorOut(message="Unauthorized")

        like = like_comment(user, input.ulid)
        if not like:
            return 400, MessageOut(error=True, message="コメントが見つかりません!")

        data = LikeOut(is_like=like.is_like, like_count=like.like_count)
        return 200, data

    @staticmethod
    @router.get("/notification", response={200: NotificationOut, 401: ErrorOut, 500: MessageOut})
    def get_notifications(request: HttpRequest):
        log.info("UserAPI get_notifications")

        user = get_user(request)
        if not user:
            return 401, ErrorOut(message="Unauthorized")

        notification = get_notification(user)
        data = NotificationOut(
            count=notification["count"],
            datas=[
                NotificationItemOut(
                    id=obj.id,
                    user_from=NotificationUserOut(
                        avatar=create_url(obj.user_from.image()),
                        nickname=obj.user_from.nickname,
                    ),
                    user_to=NotificationUserOut(
                        avatar=create_url(obj.user_to.image()) if obj.user_to else "",
                        nickname=obj.user_to.nickname if obj.user_to else "",
                    ),
                    type_no=obj.type_no,
                    type_name=obj.type_name,
                    content_object=NotificationContentOut(**get_content_object(obj)),
                    is_confirmed=obj.is_confirmed,
                )
                for obj in notification["datas"]
            ],
        )

        return 200, data

    @staticmethod
    @router.get("/channel", response={200: list[ChannelOut], 401: ErrorOut})
    def get_channels(request: HttpRequest):
        log.info("UserAPI get_channels")

        user = get_user(request)
        if user is None:
            return 401, ErrorOut(message="Unauthorized")

        channels = get_user_channels(user.id)
        data = [
            ChannelOut(ulid=str(channel.ulid), name=channel.name, is_default=channel.is_default)
            for channel in channels
        ]

        return 200, data
