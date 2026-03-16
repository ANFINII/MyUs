from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.adapter.media import convert_videos, convert_musics, convert_comics, convert_pictures, convert_blogs, convert_chats
from api.src.types.schema.channel import ChannelOut
from api.src.types.schema.common import ErrorOut, MessageOut
from api.src.types.schema.follow import FollowIn, FollowOut, FollowUserOut
from api.src.types.schema.subscribe import SubscribeIn, SubscribeOut
from api.src.types.schema.notification import NotificationContentOut, NotificationItemOut, NotificationOut, NotificationUserOut
from api.src.types.schema.user import LikeCommentIn, LikeMediaIn, LikeOut, SearchTagIn, SearchTagOut, UserOut
from api.src.types.schema.userpage import UserPageMediaOut, UserPageOut
from api.src.usecase.auth import auth_check
from api.src.usecase.channel import get_channel, get_user_channels
from api.src.usecase.follow import get_followers, get_follows, upsert_follow
from api.src.usecase.notification import get_content_object, get_notification
from api.src.usecase.subscribe import upsert_subscribe
from api.src.usecase.user import get_search_tags, get_user_data, like_comment, like_media, update_search_tags
from api.src.usecase.userpage import get_userpage_user, get_userpage_media, is_following
from api.utils.functions.index import create_url


class UserAPI:
    """ユーザーAPI"""

    router = Router()

    @staticmethod
    @router.get("/me", response={200: UserOut, 401: ErrorOut, 404: ErrorOut})
    def get_user_me(request: HttpRequest):
        log.info("UserAPI get_user_me")

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        user_data = get_user_data(user_id)
        if user_data is None:
            return 404, ErrorOut(message="Not Found")

        user = user_data.user

        data = UserOut(
            avatar=create_url(str(user.avatar)),
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

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        tags = get_search_tags(user_id)
        data = [SearchTagOut(sequence=x.sequence, name=x.name) for x in tags]
        return 200, data

    @staticmethod
    @router.put("/search_tag", response={200: MessageOut, 401: ErrorOut})
    def put_search_tag(request: HttpRequest, input: list[SearchTagIn]):
        log.info("UserAPI put_search_tag")

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        result = update_search_tags(user_id, input)
        if not result:
            return 200, MessageOut(error=True, message="更新に失敗しました")

        return 200, MessageOut(error=False, message="更新しました")

    @staticmethod
    @router.get("/follower", response={200: list[FollowUserOut], 401: ErrorOut})
    def get_followers(request: HttpRequest, search: str = ""):
        log.info("UserAPI get_followers", search=search)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        followers = get_followers(user_id, search, 100)
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

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        follows = get_follows(user_id, search, 100)
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

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        follower = get_user_data(user_id)
        if follower is None:
            return 400, MessageOut(error=True, message="ユーザーが見つかりません!")

        follow = upsert_follow(follower, input.ulid, input.is_follow)
        if follow is None:
            return 400, MessageOut(error=True, message="ユーザーが見つかりません!")

        data = FollowOut(is_follow=follow.is_follow, follower_count=follow.follower_count)
        return 200, data

    @staticmethod
    @router.post("/subscribe/channel", response={200: SubscribeOut, 400: MessageOut, 401: ErrorOut})
    def subscribe_channel(request: HttpRequest, input: SubscribeIn):
        log.info("UserAPI subscribe_channel", input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        subscribe = upsert_subscribe(user_id, input.channel_ulid, input.is_subscribe)
        if subscribe is None:
            return 400, MessageOut(error=True, message="チャンネルが見つかりません!")

        data = SubscribeOut(is_subscribe=subscribe.is_subscribe, count=subscribe.count)
        return 200, data

    @staticmethod
    @router.post("/like/media", response={200: LikeOut, 400: MessageOut, 401: ErrorOut, 500: MessageOut})
    def post_like_media(request: HttpRequest, input: LikeMediaIn):
        log.info("UserAPI like_media", input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        like = like_media(user_id, input.media_type, input.ulid)
        if like is None:
            return 400, MessageOut(error=True, message="メディアが見つかりません!")

        data = LikeOut(is_like=like.is_like, like_count=like.like_count)
        return 200, data

    @staticmethod
    @router.post("/like/comment", response={200: LikeOut, 400: MessageOut, 401: ErrorOut, 404: ErrorOut, 500: MessageOut})
    def post_like_comment(request: HttpRequest, input: LikeCommentIn):
        log.info("UserAPI like_comment", input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        like = like_comment(user_id, input.ulid)
        if like is None:
            return 400, MessageOut(error=True, message="コメントが見つかりません!")

        data = LikeOut(is_like=like.is_like, like_count=like.like_count)
        return 200, data

    @staticmethod
    @router.get("/notification", response={200: NotificationOut, 401: ErrorOut, 500: MessageOut})
    def get_notifications(request: HttpRequest):
        log.info("UserAPI get_notifications")

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        notification = get_notification(user_id)
        data = NotificationOut(
            count=notification["count"],
            datas=[
                NotificationItemOut(
                    id=obj.id,
                    user_from=NotificationUserOut(
                        avatar=create_url(obj.user_from.avatar),
                        nickname=obj.user_from.nickname,
                    ),
                    user_to=NotificationUserOut(
                        avatar=create_url(obj.user_to.avatar) if obj.user_to else "",
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

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        channels = get_user_channels(user_id)
        data = [
            ChannelOut(
                ulid=str(c.ulid),
                owner_ulid=c.owner_ulid,
                avatar=create_url(c.avatar),
                name=c.name,
                description=c.description,
                is_default=c.is_default,
            )
            for c in channels
        ]

        return 200, data

    @staticmethod
    @router.get("/userpage/{ulid}", response={200: UserPageOut, 404: ErrorOut})
    def get_userpage(request: HttpRequest, ulid: str):
        log.info("UserAPI get_userpage", ulid=ulid)

        user = get_userpage_user(ulid)
        if user is None:
            return 404, ErrorOut(message="ユーザーが見つかりません")

        channels = get_user_channels(user.user.id)
        user_id = auth_check(request)
        is_follow = is_following(user_id, user.user.id) if user_id is not None else False

        data = UserPageOut(
            avatar=create_url(user.user.avatar),
            banner=create_url(user.mypage.banner),
            nickname=user.user.nickname,
            email=user.mypage.email,
            content=user.mypage.content,
            date_joined=user.user.date_joined,
            follower_count=user.mypage.follower_count,
            following_count=user.mypage.following_count,
            is_follow=is_follow,
            channels=[
                ChannelOut(
                    ulid=str(c.ulid),
                    owner_ulid=c.owner_ulid,
                    avatar=create_url(c.avatar),
                    name=c.name,
                    description=c.description,
                    is_default=c.is_default,
                )
                for c in channels
            ],
        )

        return 200, data

    @staticmethod
    @router.get("/userpage/{ulid}/media", response={200: UserPageMediaOut, 404: ErrorOut})
    def get_userpage_media(request: HttpRequest, ulid: str, channel_ulid: str = ""):
        log.info("UserAPI get_userpage_media", ulid=ulid, channel_ulid=channel_ulid)

        user = get_userpage_user(ulid)
        if user is None:
            return 404, ErrorOut(message="ユーザーが見つかりません")

        channel_id = 0
        if channel_ulid:
            channel = get_channel(channel_ulid)
            if channel is None:
                return 404, ErrorOut(message="チャンネルが見つかりません")
            channel_id = channel.id

        media = get_userpage_media(8, "", user.user.id, channel_id=channel_id)

        data = UserPageMediaOut(
            videos=convert_videos(media.videos),
            musics=convert_musics(media.musics),
            comics=convert_comics(media.comics),
            pictures=convert_pictures(media.pictures),
            blogs=convert_blogs(media.blogs),
            chats=convert_chats(media.chats),
        )

        return 200, data
