from django.db.models import Q
from myus.db.models.es import EsProjectionProgress
from myus.domain.es.projection.data import ProjectionProgressData
from myus.domain.es.projection.interface import FilterOption, PageOption, ProjectionProgressInterface, SortOption
from myus.domain.es.projection.validation import validate
from myus.utils.common.result import FatalError, Result
from ._convert import convert_data, marshal_data
from ...common import get_save_new_ids, page_queryset, sort_ids


PROJECTION_PROGRESS_FIELDS = ["projector", "aggregate_type", "aggregate_id", "last_applied_seq"]


class ProjectionProgressRepository(ProjectionProgressInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.projector is not None:
            q_list.append(Q(projector=filter.projector))
        if filter.aggregate_type != "":
            q_list.append(Q(aggregate_type=filter.aggregate_type))
        if filter.aggregate_id != "":
            q_list.append(Q(aggregate_id=filter.aggregate_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = EsProjectionProgress.objects.filter(*q_list).order_by(order_by_key)
        qs = page_queryset(qs, page)

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[ProjectionProgressData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(EsProjectionProgress.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[ProjectionProgressData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, PROJECTION_PROGRESS_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        if len(ids) == 0:
            return Result.ok(None)
        EsProjectionProgress.objects.filter(id__in=ids).delete()
        return Result.ok(None)
