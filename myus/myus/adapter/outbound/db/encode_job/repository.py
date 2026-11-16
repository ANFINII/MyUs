from django.db.models import Q
from myus.db.models.media import EncodeJob
from myus.db.models.payment import DATETIME_MIN
from myus.domain.encode_job.data import EncodeJobData
from myus.domain.encode_job.interface import EncodeJobInterface, FilterOption, PageOption, SortOption
from myus.utils.common.result import FatalError, Result
from ._convert import convert_data, marshal_data
from ..common import get_save_new_ids, page_queryset, sort_ids


ENCODE_JOB_FIELDS = ["video_id", "publish", "processed_at", "attempts", "last_error"]


class EncodeJobRepository(EncodeJobInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.is_processed is not None:
            q_list.append(~Q(processed_at=DATETIME_MIN) if filter.is_processed else Q(processed_at=DATETIME_MIN))
        if filter.max_attempts > 0:
            q_list.append(Q(attempts__lt=filter.max_attempts))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = EncodeJob.objects.filter(*q_list).order_by(order_by_key)
        qs = page_queryset(qs, page)

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[EncodeJobData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(EncodeJob.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[EncodeJobData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, ENCODE_JOB_FIELDS)

        return Result.ok(new_ids)
