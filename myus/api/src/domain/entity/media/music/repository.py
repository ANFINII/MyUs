from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.media import Music
from api.src.domain.entity.media.music._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.entity.media.index import filter_recommend, filter_search, sort_queryset
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, SortOption


MUSIC_FIELDS = ["channel_id", "title", "content", "lyric", "music", "read", "download", "publish"]


class MusicRepository(MusicInterface):
    def queryset(self) -> QuerySet[Music]:
        return Music.objects.select_related("channel", "channel__owner").prefetch_related("like", "hashtag")

    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.publish is not None:
            q_list.append(Q(publish=filter.publish))
        if filter.owner_id:
            q_list.append(Q(channel__owner_id=filter.owner_id))
        if filter.channel_id:
            q_list.append(Q(channel_id=filter.channel_id))
        if filter.category_id:
            q_list.append(Q(category__id=filter.category_id))
        if filter.is_recommend:
            q_list.append(filter_recommend())
        if filter.search:
            q_list.append(filter_search(filter.search))
        if exclude.id:
            q_list.append(~Q(id=exclude.id))

        qs = Music.objects.filter(*q_list).distinct()
        qs, order_by_key = sort_queryset(qs, sort, filter.is_recommend)
        qs = qs.order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[MusicData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[MusicData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, Music)

        Music.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=MUSIC_FIELDS,
        )

        return new_ids

    def bulk_delete(self, ids: list[int]) -> None:
        Music.objects.filter(id__in=ids).delete()

    def is_liked(self, media_id: int, user_id: int) -> bool:
        return Music.objects.filter(id=media_id, like__id=user_id).exists()
