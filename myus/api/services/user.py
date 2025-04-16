import jwt
from django.conf import settings

from api.models import User, Follow
from api.utils.functions.index import create_url
from api.utils.functions.search import search_follow
from api.utils.functions.validation import has_alphabet, has_username, has_email, has_phone, has_postal_code, has_number, has_birthday


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

        user = User.objects.filter(id=user_id).first()
        if not user.is_active:
            return None
        return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None


def profile_check(profile) -> str | None:
    if has_email(profile["email"]):
        return "メールアドレスの形式が違います!"

    if has_username(profile["username"]):
        return "ユーザー名は半角英数字のみ入力できます!"

    if has_number(profile["last_name"]):
        return "姓に数字が含まれております!"

    if has_number(profile["first_name"]):
        return "名に数字が含まれております!"

    if has_phone(profile["phone"]):
        return "電話番号の形式が違います!"

    if has_postal_code(profile["postal_code"]):
        return "郵便番号の形式が違います!"

    if has_birthday(int(profile["year"]), int(profile["month"]), int(profile["day"])):
        return f"{profile["year"]}年{profile["month"]}月{profile["day"]}日は存在しない日付です!"


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


def get_follows(count: int, user: User, search: str | None):
    objs = Follow.objects.none
    if search:
        objs = search_follow(Follow, "follow", user, search)
    else:
        objs = Follow.objects.filter(follower=user).select_related("following__mypage").order_by("created")[:count]

    data = [{
        "avatar": create_url(obj.following.avatar.url),
        "nickname": obj.following.nickname,
        "introduction": obj.following.profile.introduction,
        "follower_count": obj.following.mypage.follower_count,
        "following_count": obj.following.mypage.following_count,
    } for obj in objs]
    return data


def get_followers(count: int, user: User, search: str | None):
    objs = Follow.objects.none
    if search:
        objs = search_follow(Follow, "follower", user, search)
    else:
        objs = Follow.objects.filter(following=user).select_related("follower__mypage").order_by("created")[:count]

    data = [{
        "avatar": create_url(obj.follower.avatar.url),
        "nickname": obj.follower.nickname,
        "introduction": obj.follower.profile.introduction,
        "follower_count": obj.follower.mypage.follower_count,
        "following_count": obj.follower.mypage.following_count,
    } for obj in objs]
    return data
