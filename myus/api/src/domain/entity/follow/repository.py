from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.users import Follow
from api.src.domain.entity.follow._convert import follow_data, marshal_follow
from api.src.domain.index import sort_ids
from api.src.domain.interface.follow.data import FollowData
from api.src.domain.interface.follow.interface import FilterOption, FollowInterface, SortOption


FOLLOW_FIELDS = ["follower_id", "following_id", "is_follow"]


class FollowRepository(FollowInterface):
    def queryset(self) -> QuerySet[Follow]:
        return Follow.objects.select_related("follower", "following")

    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.follower_id:
            q_list.append(Q(follower_id=filter.follower_id))
        if filter.following_id:
            q_list.append(Q(following_id=filter.following_id))
        if filter.search:
            q_list.append(Q(following__nickname__icontains=filter.search))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Follow.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[FollowData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [follow_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[FollowData]) -> list[FollowData]:
        if len(objs) == 0:
            return []

        Follow.objects.bulk_create(
            [marshal_follow(o) for o in objs],
            update_conflicts=True,
            update_fields=FOLLOW_FIELDS,
        )

        return self.bulk_get([o.id for o in objs])

    def count(self, filter: FilterOption) -> int:
        q_list: list[Q] = []
        if filter.follower_id:
            q_list.append(Q(follower_id=filter.follower_id))
        if filter.following_id:
            q_list.append(Q(following_id=filter.following_id))
        if filter.search:
            q_list.append(Q(following__nickname__icontains=filter.search))

        return Follow.objects.filter(*q_list).count()
