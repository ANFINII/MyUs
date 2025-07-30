from dataclasses import dataclass
from enum import Enum
from functools import reduce
from operator import and_
from django.db.models import Q
from api.models.users import Follow
from api.models.user import User
from app.modules.search import get_q_list
from api.types.data.follow import FollowOutData


@dataclass(frozen=True, slots=True)
class FilterOption:
    follower_id: int = 0
    following_id: int = 0


class SortType(Enum):
    CREATED = "created"


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class FollowDomain:
    @classmethod
    def get(cls, follower: User, following: User) -> Follow | None:
        return Follow.objects.filter(follower=follower, following=following).first()

    @classmethod
    def get_follows(cls, user_id: int, search: str | None, limit: int) -> list[Follow]:
        field_name = SortType.CREATED.value
        order_by_key = field_name if SortOption().is_asc else f'-{field_name}'
        qs = Follow.objects.filter(follower_id=user_id, is_follow=True).select_related("following__profile", "following__mypage").distinct()

        if search:
            q_list = get_q_list(search)
            query = reduce(and_, [
                Q(following__nickname__icontains=q) |
                Q(following__profile__introduction__icontains=q) for q in q_list
            ])
            qs = qs.filter(query)

        return qs.order_by(order_by_key)[:limit]

    @classmethod
    def get_followers(cls, user_id: int, search: str | None, limit: int) -> list[Follow]:
        field_name = SortType.CREATED.value
        order_by_key = field_name if SortOption().is_asc else f'-{field_name}'
        qs = Follow.objects.filter(following_id=user_id, is_follow=True).select_related("follower__profile", "follower__mypage").distinct()

        if search:
            q_list = get_q_list(search)
            search_query = reduce(and_, [
                Q(follower__nickname__icontains=q) |
                Q(follower__profile__introduction__icontains=q) for q in q_list
            ])
            qs = qs.filter(search_query)

        return qs.order_by(order_by_key)[:limit]

    @classmethod
    def create(cls, follower: User, following: User) -> None:
        Follow.objects.create(follower=follower, following=following, is_follow=True)

    @classmethod
    def update(cls, follow: Follow, is_follow: bool) -> None:
        follow.is_follow = is_follow
        follow.save(update_fields=["is_follow"])

    @classmethod
    def count(cls, filter: FilterOption) -> int:
        q_list: list[Q] = []
        if filter.follower_id:
            q_list.append(Q(follower_id=filter.follower_id, is_follow=True))
        if filter.following_id:
            q_list.append(Q(following_id=filter.following_id, is_follow=True))
        return Follow.objects.filter(*q_list).count()
