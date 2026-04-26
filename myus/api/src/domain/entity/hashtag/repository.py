from django.db import transaction
from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.hashtag import HashTag
from api.src.domain.entity.hashtag._convert import convert_data, marshal_data, marshal_through, through_model
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.interface.hashtag.data import HashtagData
from api.src.domain.interface.hashtag.interface import FilterOption, HashtagInterface, SortOption
from api.utils.enum.index import MediaType


class HashtagRepository(HashtagInterface):
    def queryset(self) -> QuerySet[HashTag]:
        return HashTag.objects.all()

    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if len(filter.ulids) > 0:
            q_list.append(Q(ulid__in=filter.ulids))
        if len(filter.names) > 0:
            q_list.append(Q(name__in=filter.names))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = HashTag.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[HashtagData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, media_type: MediaType, media_id: int, objs: list[HashtagData]) -> list[int]:
        with transaction.atomic():
            if len(objs) == 0:
                hashtag_ids: list[int] = []
            else:
                names = [o.name for o in objs]
                existing_map = {h.name: h.id for h in HashTag.objects.filter(name__in=names)}
                new_models = [marshal_data(o) for o in objs if o.name not in existing_map]
                if len(new_models) > 0:
                    get_new_ids(new_models, HashTag)
                    HashTag.objects.bulk_create(new_models, ignore_conflicts=True)
                    for m in new_models:
                        existing_map[m.name] = m.id
                hashtag_ids = [existing_map[o.name] for o in objs]

            ModelClass, fk_name = through_model(media_type)
            ModelClass.objects.filter(**{fk_name: media_id}).delete()
            if len(hashtag_ids) > 0:
                rows = [marshal_through(media_type, media_id, hid, i) for i, hid in enumerate(hashtag_ids)]
                ModelClass.objects.bulk_create(rows)

        return hashtag_ids
