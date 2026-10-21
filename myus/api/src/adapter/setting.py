from typing import assert_never
from django.http import HttpRequest
from ninja import File, Form, Router, UploadedFile
from api.modules.logger import log
from api.src.adapter.auth import auth_check
from api.src.types.schema.common import ErrorOut, ErrorType, SuccessOut
from api.src.types.schema.setting import SettingMyPageIn, SettingMyPageOut, SettingNotificationIn, SettingNotificationOut, SettingProfileIn, SettingProfileOut
from api.src.usecase.user import get_user_data, profile_check, update_mypage, update_notification, update_profile
from api.utils.common.result import FatalError, NotFoundError, ValidationError
from api.utils.functions.index import create_url
from api.utils.functions.validation import has_email


class SettingProfileAPI:
    """プロフィール設定API"""

    router = Router()

    @staticmethod
    @router.get("", response={200: SettingProfileOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest):
        log.info("SettingProfileAPI get")

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        user_data_ret = get_user_data(user_id=user_id)
        if user_data_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_data = user_data_ret.ok_value
        if user_data is None:
            return 400, ErrorOut(type=ErrorType.NOT_FOUND, message="Not Found")

        user = user_data.user
        profile = user_data.profile

        data = SettingProfileOut(
            avatar=create_url(str(user.avatar)),
            email=user.email,
            username=user.username,
            nickname=user.nickname,
            last_name=profile.last_name,
            first_name=profile.first_name,
            year=profile.birthday.year,
            month=profile.birthday.month,
            day=profile.birthday.day,
            gender=profile.gender,
            phone=profile.phone,
            country_code=profile.country_code,
            postal_code=profile.postal_code,
            prefecture=profile.prefecture,
            city=profile.city,
            street=profile.street,
            introduction=profile.introduction,
        )

        return 200, data

    @staticmethod
    @router.put("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, input: SettingProfileIn = Form(...), avatar_file: UploadedFile = File(None)):
        log.info("SettingProfileAPI put")

        message = profile_check(input)
        if len(message) > 0:
            return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_profile(user_id, input, avatar_file)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="保存しました!")


class SettingMyPageAPI:
    """マイページ設定API"""

    router = Router()

    @staticmethod
    @router.get("", response={200: SettingMyPageOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest):
        log.info("SettingMyPageAPI get")

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        user_data_ret = get_user_data(user_id=user_id)
        if user_data_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_data = user_data_ret.ok_value
        if user_data is None:
            return 400, ErrorOut(type=ErrorType.NOT_FOUND, message="Not Found")

        mypage = user_data.mypage
        user_plan = user_data.user_plan

        data = SettingMyPageOut(
            banner=create_url(str(mypage.banner)),
            ulid=user_data.user.ulid,
            nickname=user_data.user.nickname,
            email=mypage.email,
            content=mypage.content,
            follower_count=mypage.follower_count,
            following_count=mypage.following_count,
            tag_manager_id=mypage.tag_manager_id,
            plan=user_plan.plan,
            plan_start_date=user_plan.start_date,
            plan_end_date=user_plan.end_date,
            is_advertise=mypage.is_advertise,
        )

        return 200, data

    @staticmethod
    @router.put("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, input: SettingMyPageIn = Form(...), banner_file: UploadedFile = File(None)):
        log.info("SettingMyPageAPI put")

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        if has_email(input.email):
            return 400, ErrorOut(type=ErrorType.VALIDATION, message="error.emailInvalid")

        update_ret = update_mypage(user_id, input, banner_file)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="保存しました!")




class SettingNotificationAPI:
    """通知設定API"""

    router = Router()

    @staticmethod
    @router.get("", response={200: SettingNotificationOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest):
        log.info("SettingNotificationAPI get")

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        user_data_ret = get_user_data(user_id=user_id)
        if user_data_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_data = user_data_ret.ok_value
        if user_data is None:
            return 400, ErrorOut(type=ErrorType.NOT_FOUND, message="Not Found")

        notification = user_data.notification

        data = SettingNotificationOut(
            is_video=notification.is_video,
            is_music=notification.is_music,
            is_blog=notification.is_blog,
            is_comic=notification.is_comic,
            is_picture=notification.is_picture,
            is_chat=notification.is_chat,
            is_follow=notification.is_follow,
            is_reply=notification.is_reply,
            is_like=notification.is_like,
            is_views=notification.is_views,
        )

        return 200, data

    @staticmethod
    @router.put("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, input: SettingNotificationIn):
        log.info("SettingNotificationAPI put", input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_notification(user_id, input)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="保存しました!")
