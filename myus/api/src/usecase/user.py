import datetime
from dataclasses import replace
from ninja import UploadedFile
from api.db.models.user import User
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
from api.utils.functions.validation import has_alphabet, has_birthday, has_email, has_number, has_phone, has_postal_code, has_username


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
        return Result.err(NotFoundError("保存に失敗しました!"))

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
        return Result.err(NotFoundError("保存に失敗しました!"))

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
        return Result.err(NotFoundError("保存に失敗しました!"))

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
    user_repo = injector.get(UserInterface)
    media_repo = get_media_repository(media_type)
    ids_ret = media_repo.get_ids(MediaFilterOption(ulid=ulid, publish=True), ExcludeOption(), MediaSortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.err(NotFoundError("メディアが見つかりません!"))

    like_ret = user_repo.media_like(user_id, media_type, ids[0])
    if like_ret.is_err:
        return Result.err(like_ret.err_value)

    is_like, like_count = like_ret.ok_value
    return Result.ok(LikeDTO(is_like=is_like, like_count=like_count))


@Result.shield_exception()
def like_comment(user_id: int, ulid: str) -> Result[LikeDTO, FindError]:
    user_repo = injector.get(UserInterface)
    comment_repo = injector.get(CommentInterface)
    ids_ret = comment_repo.get_ids(CommentFilterOption(ulid=ulid), CommentSortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.err(NotFoundError("コメントが見つかりません!"))

    like_ret = user_repo.comment_like(user_id, ids[0])
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
        return "メールアドレスの形式が違います!"

    if has_username(data.username):
        return "ユーザー名は半角英数字のみ入力できます!"

    if has_number(data.last_name):
        return "姓に数字が含まれております!"

    if has_number(data.first_name):
        return "名に数字が含まれております!"

    if has_phone(data.phone):
        return "電話番号の形式が違います!"

    if has_postal_code(data.postal_code):
        return "郵便番号の形式が違います!"

    if has_birthday(data.year, data.month, data.day):
        return f"{data.year}年{data.month}月{data.day}日は存在しない日付です!"

    return ""


def signup_check(data: SignupIn) -> str:
    password1 = data.password1
    password2 = data.password2

    if has_email(data.email):
        return "メールアドレスの形式が違います!"

    if has_username(data.username):
        return "ユーザー名は半角英数字のみ入力できます!"

    if has_number(data.last_name):
        return "姓に数字が含まれております!"

    if has_number(data.first_name):
        return "名に数字が含まれております!"

    if has_birthday(int(data.year), int(data.month), int(data.day)):
        return f"{data.year}年{data.month}月{data.day}日は存在しない日付です!"

    if password1 != password2:
        return "パスワードが一致していません!"

    if not has_number(password1) and not has_alphabet(password1):
        return "パスワードは半角8文字以上で英数字を含む必要があります!"

    if User.objects.filter(email=data.email).exists():
        return "メールアドレスは既に登録されています!"

    if User.objects.filter(username=data.username).exists():
        return "ユーザー名は既に登録されています!"

    if User.objects.filter(nickname=data.nickname).exists():
        return "投稿者名は既に登録されています!"

    return ""
