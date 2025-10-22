import datetime
from dataclasses import asdict
from ninja import File, Form, Router, UploadedFile

from api.domain.user import UserDomain
from api.models import UserNotification
from api.modules.logger import log
from api.services.user import get_user, profile_check
from api.types.data.auth import MessageData
from api.types.data.common import ErrorData
from api.types.data.setting import MyPageInData, NotificationInData, ProfileInData, SettingMyPageInData, SettingProfileData, SettingMyPageData, SettingNotificationData, SettingProfileInData
from api.utils.functions.validation import has_email
from api.utils.functions.index import create_url, set_attr
from api.types.data.user import UserInData


class SettingProfileAPI:
    """プロフィール設定API"""

    router = Router()

    @router.get("", response={200: SettingProfileData, 401: ErrorData})
    def get(request):
        log.info("SettingProfileAPI get")

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = SettingProfileData(
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

    @router.put("", response={204: MessageData, 400: MessageData, 401: ErrorData})
    def put(request, input: SettingProfileInData = Form(...), avatar: UploadedFile = File(None)):
        log.info("SettingProfileAPI put", input=input)

        validation = profile_check(input)
        if validation:
            return 400, MessageData(error=True, message=validation)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        user_data = UserInData(
            avatar=avatar if avatar else user.avatar,
            email=input.email,
            username=input.username,
            nickname=input.nickname,
        )

        birthday = datetime.date(year=input.year, month=input.month, day=input.day)

        profile_data = ProfileInData(
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
        except Exception:
            return 400, MessageData(error=True, message="保存に失敗しました!")

        return 204, MessageData(error=False, message="保存しました!")


class SettingMyPageAPI:
    """マイページ設定API"""

    router = Router()

    @router.get("", response={200: SettingMyPageData, 401: ErrorData})
    def get(request):
        log.info("SettingMyPageAPI get")

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = SettingMyPageData(
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

    @router.put("", response={204: MessageData, 400: MessageData, 401: ErrorData})
    def put(request, input: SettingMyPageInData = Form(...), banner: UploadedFile = File(None)):
        log.info("SettingMyPageAPI put", input=input)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        if has_email(input.email):
            return 400, MessageData(error=True, message="メールアドレスの形式が違います!")

        mypage_data = MyPageInData(
            banner=banner if banner else user.mypage.banner,
            email=input.email,
            tag_manager_id=input.tag_manager_id,
            content=input.content,
            is_advertise=input.is_advertise,
        )

        try:
            UserDomain.update_mypage(user, **asdict(mypage_data))
        except Exception:
            return 400, MessageData(error=True, message="保存に失敗しました!")

        return 204, MessageData(error=False, message="保存しました!")


class SettingNotificationAPI:
    """通知設定API"""

    router = Router()

    @router.get("", response={200: SettingNotificationData, 401: ErrorData})
    def get(request):
        log.info("SettingNotificationAPI get")

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        user_notification = UserNotification.objects.filter(user=user).first()

        data = SettingNotificationData(
            is_video=user_notification.is_video,
            is_music=user_notification.is_music,
            is_comic=user_notification.is_comic,
            is_picture=user_notification.is_picture,
            is_blog=user_notification.is_blog,
            is_chat=user_notification.is_chat,
            is_follow=user_notification.is_follow,
            is_reply=user_notification.is_reply,
            is_like=user_notification.is_like,
            is_views=user_notification.is_views,
        )
        return 200, data

    @router.put("", response={204: None, 400: MessageData, 401: ErrorData})
    def put(request, input: NotificationInData):
        log.info("SettingNotificationAPI put")

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        user_notification = UserNotification.objects.filter(user=user).first()

        data = input.dict()
        [set_attr(user_notification, key, value) for key, value in data.items()]

        try:
            user_notification.save()
        except Exception:
            return 400, MessageData(error=True, message="保存に失敗しました!")

        return 204, None
