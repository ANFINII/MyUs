from dataclasses import dataclass
from enum import Enum
from functools import reduce
from operator import and_
from django.db.models import Q
from api.models.user import User
from app.modules.search import get_q_list
from api.types.data.user import AuthorData
from api.utils.functions.index import create_url


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
            user = User.objects.filter(id=id).select_related("profile", "mypage").first()

        if ulid:
            user = User.objects.filter(ulid=ulid).select_related("profile", "mypage").first()

        if not user:
            return None

        return user

    @classmethod
    def update_follower_count(cls, user: User, count: int) -> None:
        user.follower_count = count
        user.save(update_fields=["follower_count"])

    @classmethod
    def update_following_count(cls, user: User, count: int) -> None:
        user.following_count = count
        user.save(update_fields=["following_count"])

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
