from django.http import HttpRequest
from ninja import File, Form, Router, UploadedFile
from api.modules.logger import log
from api.src.types.schema.common import ErrorOut, MessageOut
from api.src.types.schema.setting import SettingMyPageIn, SettingMyPageOut, SettingNotificationIn, SettingNotificationOut, SettingProfileIn, SettingProfileOut
from api.src.usecase.user import get_user, profile_check, update_mypage, update_notification, update_profile
from api.utils.functions.index import create_url
from api.utils.functions.validation import has_email


class SettingProfileAPI:
    """プロフィール設定API"""

    router = Router()

    @staticmethod
    @router.get("", response={200: SettingProfileOut, 401: ErrorOut})
    def get(request: HttpRequest):
        log.info("SettingProfileAPI get")

        user = get_user(request)
        if user is None:
            return 401, ErrorOut(message="Unauthorized")

        data = SettingProfileOut(
            avatar=create_url(user.avatar),
            email=user.email,
            username=user.username,
            nickname=user.nickname,
            last_name=user.profile.last_name,
            first_name=user.profile.first_name,
            year=user.profile.birthday.year,
            month=user.profile.birthday.month,
            day=user.profile.birthday.day,
            gender=user.profile.gender,
            phone=user.profile.phone,
            country_code=user.profile.country_code,
            postal_code=user.profile.postal_code,
            prefecture=user.profile.prefecture,
            city=user.profile.city,
            street=user.profile.street,
            introduction=user.profile.introduction,
        )

        return 200, data

    @staticmethod
    @router.put("", response={204: MessageOut, 400: MessageOut, 401: ErrorOut})
    def put(request: HttpRequest, input: SettingProfileIn = Form(...), avatar: UploadedFile = File(None)):
        log.info("SettingProfileAPI put", input=input)

        validation = profile_check(input)
        if validation:
            return 400, MessageOut(error=True, message=validation)

        user = get_user(request)
        if user is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_profile(user, input, avatar):
            return 400, MessageOut(error=True, message="保存に失敗しました!")

        return 204, MessageOut(error=False, message="保存しました!")


class SettingMyPageAPI:
    """マイページ設定API"""

    router = Router()

    @staticmethod
    @router.get("", response={200: SettingMyPageOut, 401: ErrorOut})
    def get(request: HttpRequest):
        log.info("SettingMyPageAPI get")

        user = get_user(request)
        if user is None:
            return 401, ErrorOut(message="Unauthorized")

        data = SettingMyPageOut(
            banner=create_url(user.mypage.banner),
            nickname=user.nickname,
            email=user.mypage.email,
            content=user.mypage.content,
            follower_count=user.mypage.follower_count,
            following_count=user.mypage.following_count,
            tag_manager_id=user.mypage.tag_manager_id,
            plan=user.user_plan.plan.name,
            plan_start_date=user.user_plan.start_date,
            plan_end_date=user.user_plan.end_date,
            is_advertise=user.mypage.is_advertise,
        )

        return 200, data

    @staticmethod
    @router.put("", response={204: MessageOut, 400: MessageOut, 401: ErrorOut})
    def put(request: HttpRequest, input: SettingMyPageIn = Form(...), banner: UploadedFile = File(None)):
        log.info("SettingMyPageAPI put", input=input)

        user = get_user(request)
        if user is None:
            return 401, ErrorOut(message="Unauthorized")

        if has_email(input.email):
            return 400, MessageOut(error=True, message="メールアドレスの形式が違います!")

        if not update_mypage(user, input):
            return 400, MessageOut(error=True, message="保存に失敗しました!")

        return 204, MessageOut(error=False, message="保存しました!")


class SettingNotificationAPI:
    """通知設定API"""

    router = Router()

    @staticmethod
    @router.get("", response={200: SettingNotificationOut, 401: ErrorOut})
    def get(request: HttpRequest):
        log.info("SettingNotificationAPI get")

        user = get_user(request)
        if user is None:
            return 401, ErrorOut(message="Unauthorized")

        data = SettingNotificationOut(
            is_video=user.notification.is_video,
            is_music=user.notification.is_music,
            is_comic=user.notification.is_comic,
            is_picture=user.notification.is_picture,
            is_blog=user.notification.is_blog,
            is_chat=user.notification.is_chat,
            is_follow=user.notification.is_follow,
            is_reply=user.notification.is_reply,
            is_like=user.notification.is_like,
            is_views=user.notification.is_views,
        )

        return 200, data

    @staticmethod
    @router.put("", response={204: MessageOut, 400: MessageOut, 401: ErrorOut})
    def put(request: HttpRequest, input: SettingNotificationIn):
        log.info("SettingNotificationAPI put", input=input)

        user = get_user(request)
        if user is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_notification(user, input):
            return 400, MessageOut(error=True, message="保存に失敗しました!")

        return 204, MessageOut(error=False, message="保存しました!")
