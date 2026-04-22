from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.comment import Comment
from api.db.models.media import Video, Music, Blog, Comic, Picture, Chat
from api.db.models.message import Message
from api.db.models.notification import Notification
from api.db.models.users import Follow
from api.src.domain.entity.notification._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.interface.notification.data import NotificationData
from api.src.domain.interface.notification.interface import FilterOption, NotificationInterface, SortOption
from api.utils.enum.index import NotificationObjectType, NotificationTypeNo


NOTIFICATION_FIELDS = ["user_from_id", "user_to_id", "type_no", "type_name", "object_id", "object_type"]


class NotificationRepository(NotificationInterface):
    def queryset(self) -> QuerySet[Notification]:
        return Notification.objects.select_related("user_from", "user_to")

    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.type_no is not None:
            q_list.append(Q(type_no=filter.type_no))
        if filter.object_id:
            q_list.append(Q(object_id=filter.object_id))
        if filter.user_to_id:
            q_list.append(Q(user_to_id=filter.user_to_id))
        if filter.confirmed_user_id:
            q_list.append(Q(confirmed=filter.confirmed_user_id))
        if filter.exclude_user_id:
            q_list.append(~Q(deleted=filter.exclude_user_id))

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

        groups: dict[str, list[int]] = {}
        for n in sorted_objs:
            groups.setdefault(n.object_type, []).append(n.object_id)

        content_map: dict[str, Any] = {}
        for object_type, obj_ids in groups.items():
            match object_type:
                case NotificationObjectType.VIDEO:
                    content_map.update({f"{object_type}:{o.id}": o for o in Video.objects.filter(id__in=obj_ids)})
                case NotificationObjectType.MUSIC:
                    content_map.update({f"{object_type}:{o.id}": o for o in Music.objects.filter(id__in=obj_ids)})
                case NotificationObjectType.BLOG:
                    content_map.update({f"{object_type}:{o.id}": o for o in Blog.objects.filter(id__in=obj_ids)})
                case NotificationObjectType.COMIC:
                    content_map.update({f"{object_type}:{o.id}": o for o in Comic.objects.filter(id__in=obj_ids)})
                case NotificationObjectType.PICTURE:
                    content_map.update({f"{object_type}:{o.id}": o for o in Picture.objects.filter(id__in=obj_ids)})
                case NotificationObjectType.CHAT:
                    content_map.update({f"{object_type}:{o.id}": o for o in Chat.objects.filter(id__in=obj_ids)})
                case NotificationObjectType.FOLLOW:
                    content_map.update({f"{object_type}:{o.id}": o for o in Follow.objects.filter(id__in=obj_ids)})
                case NotificationObjectType.COMMENT:
                    content_map.update({f"{object_type}:{o.id}": o for o in Comment.objects.filter(id__in=obj_ids)})
                case NotificationObjectType.MESSAGE:
                    content_map.update({f"{object_type}:{o.id}": o for o in Message.objects.filter(id__in=obj_ids)})

        return [
            convert_data(obj, content_map.get(f"{obj.object_type}:{obj.object_id}"))
            for obj in sorted_objs
        ]

    def bulk_save(self, objs: list[NotificationData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, Notification)

        Notification.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=NOTIFICATION_FIELDS,
        )

        return new_ids

    def delete(self, type_no: NotificationTypeNo, object_id: int) -> None:
        Notification.objects.filter(type_no=type_no, object_id=object_id).delete()

    def confirm(self, ulid: str, user_id: int) -> None:
        notification = Notification.objects.filter(ulid=ulid).first()
        if notification is None:
            return
        notification.confirmed.add(user_id)

    def delete_by_user(self, ulid: str, user_id: int) -> None:
        notification = Notification.objects.filter(ulid=ulid).first()
        if notification is None:
            return
        notification.confirmed.add(user_id)
        notification.deleted.add(user_id)
