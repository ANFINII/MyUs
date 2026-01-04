import jwt
from django.conf import settings
from api.db.models import User
from api.src.domain.comment import CommentDomain
from api.src.domain.user import UserDomain
from api.src.types.data.setting.input import SettingProfileInData
from api.src.types.data.user import LikeOutData, SearchTagData
from api.utils.enum.index import MediaType
from api.utils.functions.media import get_media_domain_type
from api.utils.functions.validation import has_alphabet, has_username, has_email, has_phone, has_postal_code, has_number, has_birthday
from myus.api.src.domain.serach_tag import SearchTagDomain


def get_user(request) -> User | None:
    token = request.COOKIES.get("access_token")
    if not token:
        return None

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
        user_id = payload["user_id"]
        if not user_id:
            return None

        user = UserDomain.get(id=user_id)
        if user and not user.is_active:
            return None
        return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None


def profile_check(data: SettingProfileInData) -> str | None:
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

    return None


def signup_check(user) -> str | None:
    password1 = user["password1"]
    password2 = user["password2"]

    if has_email(user["email"]):
        return "メールアドレスの形式が違います!"

    if has_username(user["username"]):
        return "ユーザー名は半角英数字のみ入力できます!"

    if has_number(user["last_name"]):
        return "姓に数字が含まれております!"

    if has_number(user["first_name"]):
        return "名に数字が含まれております!"

    if has_birthday(int(user["year"]), int(user["month"]), int(user["day"])):
        return f"{user["year"]}年{user["month"]}月{user["day"]}日は存在しない日付です!"

    if password1 != password2:
        return "パスワードが一致していません!"

    if not has_number(password1) and not has_alphabet(password1):
        return "パスワードは半角8文字以上で英数字を含む必要があります!"

    if User.objects.filter(email=user["email"]).exists():
        return "メールアドレスは既に登録されています!"

    if User.objects.filter(username=user["username"]).exists():
        return "ユーザー名は既に登録されています!"

    if User.objects.filter(nickname=user["nickname"]).exists():
        return "投稿者名は既に登録されています!"

    return None


def get_search_tags(author_id: int) -> list[SearchTagData]:
    objs = SearchTagDomain.bulk_get(author_id)
    return [SearchTagData(sequence=obj.sequence, name=obj.name) for obj in objs]


def like_media(user: User, media_type: MediaType, ulid: str) -> LikeOutData | None:
    domain = get_media_domain_type(media_type)
    obj = domain.get(ulid=ulid, publish=True)
    if not obj:
        return None

    is_like = UserDomain.media_like(user, obj)
    like_count = obj.total_like()

    return LikeOutData(is_like=is_like, like_count=like_count)


def like_comment(user: User, ulid: str) -> LikeOutData | None:
    obj = CommentDomain.get(ulid)
    if not obj:
        return None

    is_like = UserDomain.comment_like(user, obj)
    like_count = obj.total_like()

    return LikeOutData(is_like=is_like, like_count=like_count)
