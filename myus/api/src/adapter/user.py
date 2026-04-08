from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.adapter.media import convert_videos, convert_musics, convert_comics, convert_pictures, convert_blogs, convert_chats
from api.src.types.schema.channel import ChannelOut
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.follow import FollowIn, FollowOut, FollowUserOut
from api.src.types.schema.notification import NotificationContentOut, NotificationIn, NotificationItemOut, NotificationOut, NotificationUserOut
from api.src.types.schema.user import LikeCommentIn, LikeMediaIn, LikeOut, SearchTagIn, SearchTagOut, UserOut
from api.src.types.schema.userpage import UserPageMediaOut, UserPageOut
from api.src.usecase.auth import auth_check
from api.src.usecase.channel import get_channel_data, get_user_channels
from api.src.usecase.follow import get_followers, get_follows, upsert_follow
from api.src.usecase.notification import get_notification, notification_confirm, notification_delete
from api.src.usecase.search_tag import get_search_tag_data, update_search_tags
from api.src.usecase.user import get_user_data, like_comment, like_media
from api.src.usecase.userpage import get_userpage_media, is_following
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

        user_data = get_user_data(user_id=user_id)
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

        tags = get_search_tag_data(user_id)
        data = [SearchTagOut(sequence=x.sequence, name=x.name) for x in tags]
        return 200, data

    @staticmethod
    @router.put("/search_tag", response={200: ErrorOut, 401: ErrorOut})
    def put_search_tag(request: HttpRequest, input: list[SearchTagIn]):
        log.info("UserAPI put_search_tag")

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        result = update_search_tags(user_id, input)
        if not result:
            return 200, ErrorOut(message="更新に失敗しました")

        return 200, ErrorOut(message="更新しました")

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
                ulid=x.ulid,
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
                ulid=x.ulid,
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
    @router.post("/follow/user", response={200: FollowOut, 400: ErrorOut, 401: ErrorOut, 500: ErrorOut})
    def follow_user(request: HttpRequest, input: FollowIn):
        log.info("UserAPI follow_user", input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        follower = get_user_data(user_id=user_id)
        if follower is None:
            return 400, ErrorOut(message="ユーザーが見つかりません!")

        follow = upsert_follow(follower, input.ulid, input.is_follow)
        if follow is None:
            return 400, ErrorOut(message="ユーザーが見つかりません!")

        data = FollowOut(is_follow=follow.is_follow, follower_count=follow.follower_count)
        return 200, data

    @staticmethod
    @router.post("/like/media", response={200: LikeOut, 400: ErrorOut, 401: ErrorOut, 500: ErrorOut})
    def post_like_media(request: HttpRequest, input: LikeMediaIn):
        log.info("UserAPI like_media", input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        like = like_media(user_id, input.media_type, input.ulid)
        if like is None:
            return 400, ErrorOut(message="メディアが見つかりません!")

        data = LikeOut(is_like=like.is_like, like_count=like.like_count)
        return 200, data

    @staticmethod
    @router.post("/like/comment", response={200: LikeOut, 400: ErrorOut, 401: ErrorOut, 404: ErrorOut, 500: ErrorOut})
    def post_like_comment(request: HttpRequest, input: LikeCommentIn):
        log.info("UserAPI like_comment", input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        like = like_comment(user_id, input.ulid)
        if like is None:
            return 400, ErrorOut(message="コメントが見つかりません!")

        data = LikeOut(is_like=like.is_like, like_count=like.like_count)
        return 200, data

    @staticmethod
    @router.get("/notification", response={200: NotificationOut, 401: ErrorOut, 500: ErrorOut})
    def get_notifications(request: HttpRequest):
        log.info("UserAPI get_notifications")

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        notification = get_notification(user_id)
        data = NotificationOut(
            count=notification.count,
            datas=[
                NotificationItemOut(
                    ulid=item.ulid,
                    user_from=NotificationUserOut(
                        avatar=item.user_from.avatar,
                        ulid=item.user_from.ulid,
                        nickname=item.user_from.nickname,
                    ),
                    user_to=NotificationUserOut(
                        avatar=item.user_to.avatar if item.user_to else "",
                        ulid=item.user_to.ulid if item.user_to else "",
                        nickname=item.user_to.nickname if item.user_to else "",
                    ),
                    type_no=item.type_no,
                    type_name=item.type_name,
                    content_object=NotificationContentOut(
                        id=item.content_object.id,
                        ulid=item.content_object.ulid,
                        title=item.content_object.title,
                        text=item.content_object.text,
                        read=item.content_object.read,
                    ),
                    is_confirmed=item.is_confirmed,
                )
                for item in notification.datas
            ],
        )

        return 200, data

    @staticmethod
    @router.post("/notification/confirmed", response={200: ErrorOut, 401: ErrorOut})
    def post_notification_confirmed(request: HttpRequest, input: NotificationIn):
        log.info("UserAPI post_notification_confirmed", ulid=input.ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        notification_confirm(user_id, input.ulid)
        return 200, ErrorOut(message="OK")

    @staticmethod
    @router.post("/notification/deleted", response={200: ErrorOut, 401: ErrorOut})
    def post_notification_deleted(request: HttpRequest, input: NotificationIn):
        log.info("UserAPI post_notification_deleted", ulid=input.ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        notification_delete(user_id, input.ulid)
        return 200, ErrorOut(message="OK")

    @staticmethod
    @router.get("/userpage/{ulid}", response={200: UserPageOut, 404: ErrorOut})
    def get_userpage(request: HttpRequest, ulid: str):
        log.info("UserAPI get_userpage", ulid=ulid)

        user = get_user_data(ulid=ulid)
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
                    count=c.count,
                )
                for c in channels
            ],
        )

        return 200, data

    @staticmethod
    @router.get("/userpage/{ulid}/media", response={200: UserPageMediaOut, 404: ErrorOut})
    def get_userpage_media(request: HttpRequest, ulid: str, channel_ulid: str = ""):
        log.info("UserAPI get_userpage_media", ulid=ulid, channel_ulid=channel_ulid)

        user = get_user_data(ulid=ulid)
        if user is None:
            return 404, ErrorOut(message="ユーザーが見つかりません")

        channel_id = 0
        if channel_ulid:
            channel = get_channel_data(channel_ulid)
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
