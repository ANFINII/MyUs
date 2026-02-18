from api.src.domain.interface.user.data import UserAllData
from api.src.types.data.user import AuthorData
from api.utils.functions.index import create_url


def get_author(user_map: dict[int, UserAllData], author_id: int) -> AuthorData:
    users = user_map.get(author_id)
    if users is None:
        return AuthorData(avatar="", ulid="", nickname="", follower_count=0)

    return AuthorData(
        avatar=create_url(users.user.avatar),
        ulid=users.user.ulid,
        nickname=users.user.nickname,
        follower_count=users.mypage.follower_count,
    )
