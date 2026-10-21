from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.common import AccessLog
from api.src.domain.entity.access_log._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_save_new_ids, sort_ids
from api.src.domain.interface.access_log.data import AccessLogData
from api.src.domain.interface.access_log.interface import AccessLogInterface, FilterOption, SortOption
from api.utils.common.result import FatalError, Result


ACCESS_LOG_FIELDS = ["ip_address", "type", "type_id", "updated"]


class AccessLogRepository(AccessLogInterface):
    def queryset(self) -> QuerySet[AccessLog]:
        return AccessLog.objects.all()

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.ip_address:
            q_list.append(Q(ip_address=filter.ip_address))
        if filter.type is not None:
            q_list.append(Q(type=filter.type.value))
        if filter.type_id:
            q_list.append(Q(type_id=filter.type_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = AccessLog.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[AccessLogData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[AccessLogData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, ACCESS_LOG_FIELDS)

        return Result.ok(new_ids)
