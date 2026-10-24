from django.db.models import F, Q
from django.db.models.query import QuerySet
from api.db.models.common import Advertise
from api.src.domain.entity.advertise._convert import convert_data, marshal_data, sort_field
from api.src.domain.entity.index import get_save_new_ids, sort_ids
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.domain.interface.advertise.interface import AdvertiseInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption
from api.utils.common.result import FatalError, Result


ADVERTISE_FIELDS = ["author_id", "title", "url", "content", "image", "video", "type", "period", "publish", "updated"]


def _filter_q_list(filter: FilterOption, exclude: ExcludeOption | None = None) -> list[Q]:
    q_list: list[Q] = []
    if filter.ulid:
        q_list.append(Q(ulid=filter.ulid))
    if len(filter.ulids) > 0:
        q_list.append(Q(ulid__in=filter.ulids))
    if filter.publish is not None:
        q_list.append(Q(publish=filter.publish))
    if filter.owner_id:
        q_list.append(Q(author_id=filter.owner_id))
    if filter.search:
        q_list.append(Q(title__icontains=filter.search))
    if filter.advertise_type:
        q_list.append(Q(type=filter.advertise_type))
    if exclude and exclude.id:
        q_list.append(~Q(id=exclude.id))
    return q_list


class AdvertiseRepository(AdvertiseInterface):
    def queryset(self) -> QuerySet[Advertise]:
        return Advertise.objects.all()

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> Result[list[int], FatalError]:
        qs = Advertise.objects.filter(*_filter_q_list(filter, exclude))
        field_name = sort_field(sort.sort_type)
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = qs.order_by(order_by_key)
        qs = qs[page.offset:page.offset + page.limit]
        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[AdvertiseData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[AdvertiseData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, ADVERTISE_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        Advertise.objects.filter(id__in=ids).delete()
        return Result.ok(None)

    @Result.shield_exception()
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        return Result.ok(Advertise.objects.filter(*_filter_q_list(filter)).count())

    @Result.shield_exception()
    def save_read(self, media_id: int) -> Result[int, FatalError]:
        Advertise.objects.filter(id=media_id).update(read=F("read") + 1)
        read = Advertise.objects.filter(id=media_id).values_list("read", flat=True).first()
        return Result.ok(read if read is not None else 0)
