import datetime
from django.core.files.storage import default_storage
from ninja import UploadedFile
from api.db.models.user import User
from api.modules.logger import log
from api.src.containers import injector
from api.src.domain.comment import CommentDomain, FilterOption as CommentFilterOption, SortOption as CommentSortOption
from api.src.domain.interface.user.data import MyPageData, ProfileData, UserAllData, UserData, UserNotificationData
from api.src.domain.interface.user.interface import FilterOption, UserInterface
from api.src.domain.media.index import ExcludeOption, FilterOption as MediaFilterOption, SortOption as MediaSortOption
from api.src.domain.serach_tag import FilterOption as SearchTagFilterOption, SearchTagDomain, SortOption as SearchTagSortOption
from api.src.types.data.user import LikeData, SearchTagData
from api.src.types.schema.auth import SignupIn
from api.src.types.schema.setting import SettingMyPageIn, SettingNotificationIn, SettingProfileIn
from api.utils.enum.index import ImageType, MediaType
from api.utils.functions.file import avatar_path
from api.utils.functions.media import get_media_domain_type
from api.utils.functions.validation import has_alphabet, has_birthday, has_email, has_number, has_phone, has_postal_code, has_username


def get_user_data(user_id: int) -> UserAllData | None:
    repository = injector.get(UserInterface)
    user_ids = repository.get_ids(FilterOption(id=user_id))
    if len(user_ids) == 0:
        return None

    users = repository.bulk_get(user_ids)
    user = users[0]
    if not user.user.is_active:
        return None

    return user


def save_user_data(data: UserAllData) -> bool:
    repository = injector.get(UserInterface)
    try:
        repository.bulk_save([data])
        return True
    except Exception as e:
        log.error("save_user_data error", exc=e)
        return False


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


def get_search_tags(author_id: int) -> list[SearchTagData]:
    ids = SearchTagDomain.get_ids(SearchTagFilterOption(author_id=author_id), SearchTagSortOption())
    objs = SearchTagDomain.bulk_get(ids)
    return [SearchTagData(sequence=obj.sequence, name=obj.name) for obj in objs]


def like_media(user_id: int, media_type: MediaType, ulid: str) -> LikeData | None:
    repository = injector.get(UserInterface)
    domain = get_media_domain_type(media_type)
    ids = domain.get_ids(MediaFilterOption(ulid=ulid, publish=True), ExcludeOption(), MediaSortOption())
    if len(ids) == 0:
        return None

    obj = domain.bulk_get(ids)[0]
    is_like = repository.media_like(user_id, obj)
    like_count = obj.total_like()

    return LikeData(is_like=is_like, like_count=like_count)


def like_comment(user_id: int, ulid: str) -> LikeData | None:
    repository = injector.get(UserInterface)
    ids = CommentDomain.get_ids(CommentFilterOption(ulid=ulid), CommentSortOption())
    if len(ids) == 0:
        return None

    obj = CommentDomain.bulk_get(ids)[0]
    is_like = repository.comment_like(user_id, obj)
    like_count = obj.total_like()

    return LikeData(is_like=is_like, like_count=like_count)


def save_upload(file: UploadedFile, ulid: str) -> str:
    path = avatar_path(ImageType.USER, ulid, file.name or "upload")
    return default_storage.save(path, file)


def update_profile(user_id: int, input: SettingProfileIn, avatarFile: UploadedFile) -> bool:
    data = get_user_data(user_id)
    if data is None:
        return False

    base = data.user
    avatar = save_upload(avatarFile, base.ulid) if avatarFile else base.avatar

    user = UserData(
        id=base.id,
        ulid=base.ulid,
        avatar=avatar,
        password=base.password,
        email=input.email,
        username=input.username,
        nickname=input.nickname,
        is_active=base.is_active,
        is_staff=base.is_staff,
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

    updated_data = UserAllData(
        user=user,
        profile=profile,
        mypage=data.mypage,
        notification=data.notification,
        user_plan=data.user_plan,
    )

    return save_user_data(updated_data)


def update_mypage(user_id: int, input: SettingMyPageIn, bannerFile: UploadedFile) -> bool:
    data = get_user_data(user_id)
    if data is None:
        return False

    banner = save_upload(bannerFile, data.user.ulid) if bannerFile else data.mypage.banner

    mypage = MyPageData(
        banner=banner,
        email=input.email,
        content=input.content,
        follower_count=data.mypage.follower_count,
        following_count=data.mypage.following_count,
        tag_manager_id=input.tag_manager_id,
        is_advertise=input.is_advertise,
    )

    updated_data = UserAllData(
        user=data.user,
        profile=data.profile,
        mypage=mypage,
        notification=data.notification,
        user_plan=data.user_plan,
    )

    return save_user_data(updated_data)


def update_notification(user_id: int, input: SettingNotificationIn) -> bool:
    data = get_user_data(user_id)
    if data is None:
        return False

    notification = UserNotificationData(
        is_video=input.is_video,
        is_music=input.is_music,
        is_comic=input.is_comic,
        is_picture=input.is_picture,
        is_blog=input.is_blog,
        is_chat=input.is_chat,
        is_follow=input.is_follow,
        is_reply=input.is_reply,
        is_like=input.is_like,
        is_views=input.is_views,
    )

    updated_data = UserAllData(
        user=data.user,
        profile=data.profile,
        mypage=data.mypage,
        notification=notification,
        user_plan=data.user_plan,
    )

    return save_user_data(updated_data)
