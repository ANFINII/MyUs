from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.media import Picture
from api.src.domain.entity.media.picture._convert import convert_data, marshal_data
from api.src.domain.entity.index import sort_ids
from api.src.domain.interface.media.picture.data import PictureData
from api.src.domain.interface.media.picture.interface import PictureInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, SortOption


PICTURE_FIELDS = ["channel_id", "title", "content", "image", "read", "publish"]


class PictureRepository(PictureInterface):
    def queryset(self) -> QuerySet[Picture]:
        return Picture.objects.select_related("channel").prefetch_related("like")

    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.publish:
            q_list.append(Q(publish=filter.publish))
        if filter.category_id:
            q_list.append(Q(category__id=filter.category_id))
        if filter.search:
            q_list.append(Q(title__icontains=filter.search))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Picture.objects.filter(*q_list).order_by(order_by_key)

        if exclude.id is not None:
            qs = qs.exclude(id=exclude.id)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[PictureData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[PictureData]) -> None:
        if len(objs) == 0:
            return

        Picture.objects.bulk_create(
            [marshal_data(o) for o in objs],
            update_conflicts=True,
            update_fields=PICTURE_FIELDS,
        )
