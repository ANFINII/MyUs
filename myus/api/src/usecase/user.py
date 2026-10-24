import datetime
from dataclasses import replace
from ninja import UploadedFile
from api.src.injectors.container import injector
from api.src.domain.interface.comment.interface import CommentInterface, FilterOption as CommentFilterOption, SortOption as CommentSortOption
from api.src.domain.interface.media.index import ExcludeOption, FilterOption as MediaFilterOption, PageOption, SortOption as MediaSortOption
from api.src.domain.interface.notification.interface import NotificationInterface
from api.src.domain.interface.user.data import ProfileData, UserAllData, UserNotificationData
from api.src.domain.interface.user.interface import FilterOption, UserInterface
from api.src.types.dto.user import AuthorDTO, LikeDTO
from api.src.types.schema.auth import SignupIn
from api.src.types.schema.setting import SettingMyPageIn, SettingNotificationIn, SettingProfileIn
from api.src.usecase.notification import create_notification
from api.utils.common.result import FatalError, FindError, InputError, NotFoundError, Result
from api.utils.enum.media import MediaType
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from api.utils.enum.upload import ImageUpload
from api.utils.functions.index import create_url
from api.utils.functions.media import get_media_repository, save_upload, validate_uploads
from api.utils.functions.validation import PASSWORD_MIN_LENGTH, has_alphabet, has_birthday, has_email, has_number, has_phone, has_postal_code, has_username
from api.utils.plan import PlanDef, get_plan


@Result.shield_exception()
def get_user_data(user_id: int = 0, ulid: str = "") -> Result[UserAllData | None, FatalError]:
    repo = injector.get(UserInterface)
    ids_ret = repo.get_ids(FilterOption(id=user_id, ulid=ulid))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.ok(None)

    users_ret = repo.bulk_get(ids)
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    return Result.ok(users[0])


@Result.shield_exception()
def get_user_plan(user_id: int) -> Result[PlanDef | None, FatalError]:
    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        return Result.ok(None)

    return Result.ok(get_plan(user.user_plan.plan))


@Result.shield_exception()
def save_user_data(data: UserAllData) -> Result[None, FatalError]:
    repo = injector.get(UserInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_author_data(user_id: int) -> Result[AuthorDTO, FatalError]:
    ret = get_user_data(user_id=user_id)
    if ret.is_err:
        return Result.err(ret.err_value)

    user = ret.ok_value
    if user is None:
        return Result.ok(AuthorDTO(avatar="", ulid="", nickname="", follower_count=0))

    data = AuthorDTO(
        avatar=create_url(user.user.avatar),
        ulid=user.user.ulid,
        nickname=user.user.nickname,
        follower_count=user.mypage.follower_count,
    )

    return Result.ok(data)


@Result.shield_exception()
def get_author_data_map(ids: list[int]) -> Result[dict[int, AuthorDTO], FatalError]:
    if len(ids) == 0:
        return Result.ok({})

    repo = injector.get(UserInterface)
    ret = repo.bulk_get(ids)
    if ret.is_err:
        return Result.err(ret.err_value)

    authors = ret.ok_value
    author_map: dict[int, AuthorDTO] = {id: AuthorDTO(avatar="", ulid="", nickname="", follower_count=0) for id in ids}
    for author in authors:
        author_map[author.user.id] = AuthorDTO(
            avatar=create_url(author.user.avatar),
            ulid=author.user.ulid,
            nickname=author.user.nickname,
            follower_count=author.mypage.follower_count,
        )

    return Result.ok(author_map)


@Result.shield_exception()
def update_profile(user_id: int, input: SettingProfileIn, avatar_file: UploadedFile) -> Result[None, InputError]:
    upload_ret = validate_uploads([(avatar_file, ImageUpload.USER)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    data_ret = get_user_data(user_id)
    if data_ret.is_err:
        return Result.err(data_ret.err_value)

    data = data_ret.ok_value
    if data is None:
        return Result.err(NotFoundError("error.saveFailed"))

    base = data.user
    avatar = save_upload(avatar_file, ImageUpload.USER, base.ulid) if avatar_file else base.avatar

    user = replace(
        base,
        avatar=avatar,
        email=input.email,
        username=input.username,
        nickname=input.nickname,
    )

    profile = ProfileData(
        last_name=input.last_name,
        first_name=input.first_name,
        gender=input.gender,
        birthday=datetime.date(year=input.year, month=input.month, day=input.day),
        phone=input.phone,
        country_code="JP",
        postal_code=input.postal_code,
        prefecture=input.prefecture,
        city=input.city,
        street=input.street,
        introduction=input.introduction,
    )

    save_data = replace(data, user=user, profile=profile)
    save_ret = save_user_data(save_data)
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def update_mypage(user_id: int, input: SettingMyPageIn, banner_file: UploadedFile) -> Result[None, InputError]:
    upload_ret = validate_uploads([(banner_file, ImageUpload.USER)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    data_ret = get_user_data(user_id)
    if data_ret.is_err:
        return Result.err(data_ret.err_value)

    data = data_ret.ok_value
    if data is None:
        return Result.err(NotFoundError("error.saveFailed"))

    banner = save_upload(banner_file, ImageUpload.USER, data.user.ulid) if banner_file else data.mypage.banner

    mypage = replace(
        data.mypage,
        banner=banner,
        email=input.email,
        content=input.content,
        tag_manager_id=input.tag_manager_id,
        is_advertise=input.is_advertise,
    )

    save_data = replace(data, mypage=mypage)
    save_ret = save_user_data(save_data)
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def update_notification(user_id: int, input: SettingNotificationIn) -> Result[None, FindError]:
    data_ret = get_user_data(user_id)
    if data_ret.is_err:
        return Result.err(data_ret.err_value)

    data = data_ret.ok_value
    if data is None:
        return Result.err(NotFoundError("error.saveFailed"))

    notification = UserNotificationData(
        is_video=input.is_video,
        is_music=input.is_music,
        is_blog=input.is_blog,
        is_comic=input.is_comic,
        is_picture=input.is_picture,
        is_chat=input.is_chat,
        is_follow=input.is_follow,
        is_reply=input.is_reply,
        is_like=input.is_like,
        is_views=input.is_views,
    )

    save_data = replace(data, notification=notification)
    save_ret = save_user_data(save_data)
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def like_media(user_id: int, media_type: MediaType, ulid: str) -> Result[LikeDTO, FindError]:
    repo = injector.get(UserInterface)
    media_repo = get_media_repository(media_type)
    ids_ret = media_repo.get_ids(MediaFilterOption(ulid=ulid, publish=True), ExcludeOption(), MediaSortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.err(NotFoundError("error.mediaNotFound"))

    like_ret = repo.media_like(user_id, media_type, ids[0])
    if like_ret.is_err:
        return Result.err(like_ret.err_value)

    is_like, like_count = like_ret.ok_value
    return Result.ok(LikeDTO(is_like=is_like, like_count=like_count))


@Result.shield_exception()
def like_comment(user_id: int, ulid: str) -> Result[LikeDTO, FindError]:
    repo = injector.get(UserInterface)
    comment_repo = injector.get(CommentInterface)
    ids_ret = comment_repo.get_ids(CommentFilterOption(ulid=ulid), CommentSortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.err(NotFoundError("error.commentNotFound"))

    like_ret = repo.comment_like(user_id, ids[0])
    if like_ret.is_err:
        return Result.err(like_ret.err_value)

    is_like, like_count = like_ret.ok_value
    if is_like:
        comments_ret = comment_repo.bulk_get(ids)
        if comments_ret.is_err:
            return Result.err(comments_ret.err_value)

        comments = comments_ret.ok_value
        comment = comments[0]
        create_ret = create_notification(user_id, comment.author_id, NotificationTypeNo.LIKE, comment.id, NotificationObjectType.COMMENT)
        if create_ret.is_err:
            return Result.err(create_ret.err_value)
    else:
        notification_repo = injector.get(NotificationInterface)
        delete_ret = notification_repo.delete(NotificationTypeNo.LIKE, NotificationObjectType.COMMENT, ids[0], user_id)
        if delete_ret.is_err:
            return Result.err(delete_ret.err_value)

    return Result.ok(LikeDTO(is_like=is_like, like_count=like_count))


def profile_check(data: SettingProfileIn) -> str:
    if has_email(data.email):
        return "error.emailInvalid"

    if has_username(data.username):
        return "error.usernameInvalid"

    if has_number(data.last_name):
        return "error.lastNameInvalid"

    if has_number(data.first_name):
        return "error.firstNameInvalid"

    if has_phone(data.phone):
        return "error.phoneInvalid"

    if has_postal_code(data.postal_code):
        return "error.postalCodeInvalid"

    if has_birthday(data.year, data.month, data.day):
        return "error.birthdayInvalid"

    return ""


@Result.shield_exception()
def signup_check(data: SignupIn) -> Result[str, FatalError]:
    password1 = data.password1
    password2 = data.password2

    if has_email(data.email):
        return Result.ok("error.emailInvalid")

    if has_username(data.username):
        return Result.ok("error.usernameInvalid")

    if has_number(data.last_name):
        return Result.ok("error.lastNameInvalid")

    if has_number(data.first_name):
        return Result.ok("error.firstNameInvalid")

    if has_birthday(int(data.year), int(data.month), int(data.day)):
        return Result.ok("error.birthdayInvalid")

    if password1 != password2:
        return Result.ok("error.passwordMismatch")

    if len(password1) < PASSWORD_MIN_LENGTH or not has_number(password1) or not has_alphabet(password1):
        return Result.ok("error.passwordInvalid")

    repo = injector.get(UserInterface)
    registered_checks = [
        (data.email, FilterOption(email=data.email), "error.emailTaken"),
        (data.username, FilterOption(username=data.username), "error.usernameTaken"),
        (data.nickname, FilterOption(nickname=data.nickname), "error.nicknameTaken"),
    ]
    for value, filter, message in registered_checks:
        if len(value) == 0:
            continue

        ids_ret = repo.get_ids(filter)
        if ids_ret.is_err:
            return Result.err(ids_ret.err_value)

        ids = ids_ret.ok_value
        if len(ids) > 0:
            return Result.ok(message)

    return Result.ok("")
