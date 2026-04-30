from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.common import Advertise
from api.src.domain.entity.advertise._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.domain.interface.advertise.interface import AdvertiseInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption


ADVERTISE_FIELDS = ["author_id", "title", "url", "content", "image", "video", "read", "type", "period", "publish"]


def _filter_q_list(filter: FilterOption, exclude: ExcludeOption | None = None) -> list[Q]:
    q_list: list[Q] = []
    if filter.ulid:
        q_list.append(Q(ulid=filter.ulid))
    if filter.publish is not None:
        q_list.append(Q(publish=filter.publish))
    if filter.owner_id:
        q_list.append(Q(author_id=filter.owner_id))
    if filter.search:
        q_list.append(Q(title__icontains=filter.search))
    if exclude and exclude.id:
        q_list.append(~Q(id=exclude.id))
    return q_list


class AdvertiseRepository(AdvertiseInterface):
    def queryset(self) -> QuerySet[Advertise]:
        return Advertise.objects.all()

    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> list[int]:
        qs = Advertise.objects.filter(*_filter_q_list(filter, exclude))
        order_by_key = "id" if sort.is_asc else "-id"
        qs = qs.order_by(order_by_key)
        qs = qs[page.offset:page.offset + page.limit]
        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[AdvertiseData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[AdvertiseData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, Advertise)

        Advertise.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=ADVERTISE_FIELDS,
        )

        return new_ids

    def bulk_delete(self, ids: list[int]) -> None:
        Advertise.objects.filter(id__in=ids).delete()

    def count(self, filter: FilterOption) -> int:
        return Advertise.objects.filter(*_filter_q_list(filter)).count()
