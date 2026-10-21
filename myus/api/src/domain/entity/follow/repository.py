from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.users import Follow
from api.src.domain.entity.follow._convert import convert_data, marshal_data
from api.src.domain.entity.index import insert_new_models, sort_ids
from api.src.domain.interface.follow.data import FollowData
from api.src.domain.interface.follow.interface import FilterOption, FollowInterface, SortOption
from api.utils.common.result import FatalError, Result


FOLLOW_FIELDS = ["follower_id", "following_id", "is_follow"]


class FollowRepository(FollowInterface):
    def queryset(self) -> QuerySet[Follow]:
        return Follow.objects.select_related("follower", "following")

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.follower_id:
            q_list.append(Q(follower_id=filter.follower_id))
        if filter.following_id:
            q_list.append(Q(following_id=filter.following_id))
        if filter.is_follow is not None:
            q_list.append(Q(is_follow=filter.is_follow))
        if filter.search:
            q_list.append(Q(following__nickname__icontains=filter.search))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Follow.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[FollowData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[FollowData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = insert_new_models(models)

        Follow.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=FOLLOW_FIELDS,
        )

        return Result.ok(new_ids)

    @Result.shield_exception()
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        q_list: list[Q] = []
        if filter.follower_id:
            q_list.append(Q(follower_id=filter.follower_id))
        if filter.following_id:
            q_list.append(Q(following_id=filter.following_id))
        if filter.is_follow is not None:
            q_list.append(Q(is_follow=filter.is_follow))
        if filter.search:
            q_list.append(Q(following__nickname__icontains=filter.search))

        return Result.ok(Follow.objects.filter(*q_list).count())
