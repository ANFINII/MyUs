import jwt
from django.conf import settings
from api.db.models.user import User
from api.src.domain.comment import CommentDomain, FilterOption as CommentFilterOption, SortOption as CommentSortOption
from api.src.domain.serach_tag import SearchTagDomain, FilterOption as SearchTagFilterOption, SortOption as SearchTagSortOption
from api.src.domain.media.index import FilterOption as MediaFilterOption, SortOption as MediaSortOption, ExcludeOption
from api.src.domain.user import FilterOption, SortOption, UserDomain
# from api.src.domain.user.data import user_data
# from api.src.domain.user.type import UserData
from api.src.types.data.user import LikeData, SearchTagData
from api.src.types.schema.auth import SignupIn
from api.src.types.schema.setting import SettingProfileIn
from api.utils.enum.index import MediaType
from api.utils.functions.media import get_media_domain_type
from api.utils.functions.validation import has_alphabet, has_username, has_email, has_phone, has_postal_code, has_number, has_birthday


def get_user(request) -> User | None:
    token = request.COOKIES.get("access_token")
    if token is None:
        return None

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
        user_id = payload["user_id"]
        if user_id is None:
            return None

        user_ids = UserDomain.get_ids(FilterOption(id=user_id), SortOption())
        if len(user_ids) == 0:
            return None

        user = UserDomain.bulk_get(user_ids)[0]
        if not user.is_active:
            return None
        return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None


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


def like_media(user: User, media_type: MediaType, ulid: str) -> LikeData | None:
    domain = get_media_domain_type(media_type)
    ids = domain.get_ids(MediaFilterOption(ulid=ulid, publish=True), ExcludeOption(), MediaSortOption())
    if len(ids) == 0:
        return None

    obj = domain.bulk_get(ids)[0]
    is_like = UserDomain.media_like(user, obj)
    like_count = obj.total_like()

    return LikeData(is_like=is_like, like_count=like_count)


def like_comment(user: User, ulid: str) -> LikeData | None:
    ids = CommentDomain.get_ids(CommentFilterOption(ulid=ulid), CommentSortOption())
    if len(ids) == 0:
        return None

    obj = CommentDomain.bulk_get(ids)[0]
    is_like = UserDomain.comment_like(user, obj)
    like_count = obj.total_like()

    return LikeData(is_like=is_like, like_count=like_count)
