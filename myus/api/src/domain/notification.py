from dataclasses import dataclass
from enum import Enum
from django.db.models import Q
from api.db.models.notification import Notification
from api.src.domain.index import sort_ids
from api.utils.enum.index import NotificationTypeNo
from api.utils.functions.index import set_attr


class SortType(Enum):
    CREATED = "created"


@dataclass(frozen=True, slots=True)
class FilterOption:
    type_no: NotificationTypeNo | None = None
    object_id: int = 0
    user_to_id: int = 0


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class NotificationDomain:
    @classmethod
    def queryset(cls):
        return Notification.objects.select_related("user_from", "user_to")

    @classmethod
    def get_ids(cls, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.type_no:
            q_list.append(Q(type_no=filter.type_no))
        if filter.object_id:
            q_list.append(Q(object_id=filter.object_id))
        if filter.user_to_id:
            q_list.append(Q(user_to_id=filter.user_to_id))

        field_name = sort.sort_type.value
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Notification.objects.filter(*q_list).order_by(order_by_key)

        if limit:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    @classmethod
    def bulk_get(cls, ids: list[int]) -> list[Notification]:
        if len(ids) == 0:
            return []

        objs = cls.queryset().filter(id__in=ids)
        return sort_ids(objs, ids)

    @classmethod
    def create(cls, **kwargs) -> Notification:
        return Notification.objects.create(**kwargs)

    @classmethod
    def update(cls, obj: Notification, **kwargs) -> None:
        if not kwargs:
            return

        [set_attr(obj, key, value) for key, value in kwargs.items()]
        obj.save(update_fields=list(kwargs.keys()))

    @classmethod
    def delete(cls, type_no: NotificationTypeNo, object_id: int) -> None:
        obj = Notification.objects.filter(type_no=type_no, object_id=object_id)
        obj.delete()
        return

    #     NotificationOutData(
    #         id=obj.id,
    #         user_from=obj.user_from,
    #         user_to=obj.user_to,
    #         type_no=obj.type_no,
    #         type_name=obj.type_name,
    #         object_id=obj.object_id,
    #         object_type=obj.object_type,
    #     )
