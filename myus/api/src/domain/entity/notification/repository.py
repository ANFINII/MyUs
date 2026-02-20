from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.notification import Notification
from api.src.domain.entity.notification._convert import convert_data, marshal_data
from api.src.domain.entity.index import sort_ids
from api.src.domain.interface.notification.data import NotificationData
from api.src.domain.interface.notification.interface import FilterOption, NotificationInterface, SortOption
from api.utils.enum.index import NotificationTypeNo


NOTIFICATION_FIELDS = ["user_from_id", "user_to_id", "type_no", "type_name", "object_id", "object_type"]


class NotificationRepository(NotificationInterface):
    def queryset(self) -> QuerySet[Notification]:
        return Notification.objects.select_related("user_from", "user_to")

    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.type_no is not None:
            q_list.append(Q(type_no=filter.type_no))
        if filter.object_id:
            q_list.append(Q(object_id=filter.object_id))
        if filter.user_to_id:
            q_list.append(Q(user_to_id=filter.user_to_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Notification.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[NotificationData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[NotificationData]) -> None:
        if len(objs) == 0:
            return None

        Notification.objects.bulk_create(
            [marshal_data(o) for o in objs],
            update_conflicts=True,
            update_fields=NOTIFICATION_FIELDS,
        )

        return None

    def delete(self, type_no: NotificationTypeNo, object_id: int) -> None:
        Notification.objects.filter(type_no=type_no, object_id=object_id).delete()
