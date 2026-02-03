import datetime
from dataclasses import asdict
from django.http import HttpRequest
from ninja import File, Form, Router, UploadedFile
from api.modules.logger import log
from api.src.domain.user import UserDomain
from api.src.types.data.setting import MyPageData, ProfileData
from api.src.types.data.user import UserInData
from api.src.types.schema.common import ErrorOut, MessageOut
from api.src.types.schema.setting import SettingMyPageIn, SettingMyPageOut, SettingNotificationIn, SettingNotificationOut, SettingProfileIn, SettingProfileOut
from api.src.usecase.user import get_user, profile_check
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
            avatar=create_url(user.image()),
            email=user.email,
            username=user.username,
            nickname=user.nickname,
            last_name=user.profile.last_name,
            first_name=user.profile.first_name,
            year=user.year(),
            month=user.month(),
            day=user.day(),
            gender=user.gender(),
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

        user_data = UserInData(
            avatar=avatar if avatar else user.avatar,
            email=input.email,
            username=input.username,
            nickname=input.nickname,
        )

        birthday = datetime.date(year=input.year, month=input.month, day=input.day)

        profile_data = ProfileData(
            last_name=input.last_name,
            first_name=input.first_name,
            gender=input.gender,
            birthday=birthday,
            phone=input.phone,
            postal_code=input.postal_code,
            prefecture=input.prefecture,
            city=input.city,
            street=input.street,
            introduction=input.introduction,
        )

        try:
            UserDomain.update(user, **asdict(user_data))
            UserDomain.update_profile(user, **asdict(profile_data))
        except Exception as e:
            log.error("SettingProfileAPI put error", error=e)
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
            banner=create_url(user.banner()),
            nickname=user.nickname,
            email=user.mypage.email,
            content=user.mypage.content,
            follower_count=user.mypage.follower_count,
            following_count=user.mypage.following_count,
            tag_manager_id=user.mypage.tag_manager_id,
            plan=user.plan(),
            plan_start_date=user.plan_start_date(),
            plan_end_date=user.plan_end_date(),
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

        mypage_data = MyPageData(
            banner=banner if banner else user.mypage.banner,
            email=input.email,
            tag_manager_id=input.tag_manager_id,
            content=input.content,
            is_advertise=input.is_advertise,
        )

        try:
            UserDomain.update_mypage(user, **asdict(mypage_data))
        except Exception as e:
            log.error("SettingMyPageAPI put error", error=e)
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

        try:
            UserDomain.update_notification(user, **input.model_dump())
        except Exception as e:
            log.error("SettingNotificationAPI put error", error=e)
            return 400, MessageOut(error=True, message="保存に失敗しました!")

        return 204, MessageOut(error=False, message="保存しました!")
