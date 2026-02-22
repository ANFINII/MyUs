from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.media import Video
from api.src.domain.entity.media.video._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, SortOption


VIDEO_FIELDS = ["channel_id", "title", "content", "image", "video", "convert", "read", "publish"]


class VideoRepository(VideoInterface):
    def queryset(self) -> QuerySet[Video]:
        return Video.objects.select_related("channel").prefetch_related("like", "hashtag")

    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.publish is not None:
            q_list.append(Q(publish=filter.publish))
        if filter.category_id:
            q_list.append(Q(category__id=filter.category_id))
        if filter.search:
            q_list.append(Q(title__icontains=filter.search))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Video.objects.filter(*q_list).order_by(order_by_key)

        if exclude.id is not None:
            qs = qs.exclude(id=exclude.id)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[VideoData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[VideoData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, Video)

        Video.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=VIDEO_FIELDS,
        )

        return new_ids

    def is_liked(self, media_id: int, user_id: int) -> bool:
        return Video.objects.filter(id=media_id, like__id=user_id).exists()
