from dataclasses import dataclass
from enum import Enum
from api.models.user import User
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

    # @classmethod
    # def bulk_get(cls, search: str | None = None, limit: int = 100, sort_option: SortOption | None = None) -> list[AuthorData]:
    #     if sort_option is None:
    #         sort_option = SortOption()

    #     field_name = sort_option.sort_type.value
    #     order_by_key = field_name if sort_option.is_asc else f'-{field_name}'
    #     qs = User.objects.filter(is_active=True).select_related("profile", "mypage").distinct()

    #     if search:
    #         q_list = get_q_list(search)
    #         query = reduce(and_, [
    #             Q(nickname__icontains=q) |
    #             Q(profile__introduction__icontains=q) |
    #             Q(email__icontains=q) for q in q_list
    #         ])
    #         qs = qs.filter(query)

    #     objs = qs.order_by(order_by_key)[:limit]

    #     return [
    #         AuthorData(
    #             avatar=create_url(obj.avatar.url) if obj.avatar else create_url(obj.img),
    #             nickname=obj.nickname,
    #             follower_count=obj.mypage.follower_count,
    #         ) for obj in objs
    #     ]
