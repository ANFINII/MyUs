from dataclasses import dataclass
from enum import Enum
from api.db.models.user import User
from api.utils.functions.index import set_attr


class SortType(Enum):
    CREATED = "date_joined"
    NICKNAME = "nickname"


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class UserDomain:
    @classmethod
    def get(cls, id: int | None = None, ulid: str | None = None) -> User | None:
        if id:
            user = User.objects.filter(id=id).select_related("profile", "mypage", "notification").first()

        if ulid:
            user = User.objects.filter(ulid=ulid).select_related("profile", "mypage", "notification").first()

        if not user:
            return None

        return user

    @classmethod
    def create(cls, **kwargs) -> User:
       return User.objects.create_user(**kwargs)

    @classmethod
    def update(cls, user: User, **kwargs) -> None:
        if not kwargs:
            return

        [set_attr(user, key, value) for key, value in kwargs.items()]
        user.save(update_fields=list(kwargs.keys()))

    @classmethod
    def update_profile(cls, user: User, **kwargs) -> None:
        if not kwargs:
            return

        [set_attr(user.profile, key, value) for key, value in kwargs.items()]
        user.profile.save(update_fields=list(kwargs.keys()))

    @classmethod
    def update_mypage(cls, user: User, **kwargs) -> None:
        if not kwargs:
            return

        [set_attr(user.mypage, key, value) for key, value in kwargs.items()]
        user.mypage.save(update_fields=list(kwargs.keys()))

    @classmethod
    def update_notification(cls, user: User, **kwargs) -> None:
        if not kwargs:
            return

        [set_attr(user.notification, key, value) for key, value in kwargs.items()]
        user.notification.save(update_fields=list(kwargs.keys()))
