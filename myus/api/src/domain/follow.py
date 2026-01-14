from dataclasses import dataclass
from enum import Enum
from functools import reduce
from operator import and_
from django.db.models import Q
from api.db.models.users import Follow
from api.src.domain.index import sort_ids
from api.utils.functions.index import set_attr
from api.utils.functions.search import get_q_list


@dataclass(frozen=True, slots=True)
class FilterOption:
    follower_id: int = 0
    following_id: int = 0
    search: str = ""


class SortType(Enum):
    CREATED = "created"


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class FollowDomain:
    @classmethod
    def queryset(cls):
        return Follow.objects.select_related(
            "follower__profile", "follower__mypage",
            "following__profile", "following__mypage"
        )

    @classmethod
    def get_ids(cls, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []

        if filter.follower_id:
            q_list.append(Q(follower_id=filter.follower_id))
        if filter.following_id:
            q_list.append(Q(following_id=filter.following_id))

        is_pair = filter.follower_id and filter.following_id
        if not is_pair:
            q_list.append(Q(is_follow=True))

        if filter.search and filter.follower_id and not is_pair:
            search_list = get_q_list(filter.search)
            query = reduce(and_, [
                Q(following__nickname__icontains=q) |
                Q(following__profile__introduction__icontains=q) for q in search_list
            ])
            q_list.append(query)

        if filter.search and filter.following_id and not is_pair:
            search_list = get_q_list(filter.search)
            query = reduce(and_, [
                Q(follower__nickname__icontains=q) |
                Q(follower__profile__introduction__icontains=q) for q in search_list
            ])
            q_list.append(query)

        field_name = sort.sort_type.value
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Follow.objects.filter(*q_list).order_by(order_by_key)

        if limit:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    @classmethod
    def bulk_get(cls, ids: list[int]) -> list[Follow]:
        if not ids:
            return []

        objs = cls.queryset().filter(id__in=ids)
        return sort_ids(objs, ids)

    @classmethod
    def create(cls, **kwargs) -> Follow:
        return Follow.objects.create(**kwargs)

    @classmethod
    def update(cls, obj: Follow, **kwargs) -> None:
        if not kwargs:
            return

        [set_attr(obj, key, value) for key, value in kwargs.items()]
        obj.save(update_fields=list(kwargs.keys()))
        return

    @classmethod
    def count(cls, filter: FilterOption) -> int:
        qs = Follow.objects.filter(is_follow=True)
        if filter.follower_id:
            qs = qs.filter(follower_id=filter.follower_id)
        if filter.following_id:
            qs = qs.filter(following_id=filter.following_id)
        return qs.count()
