from typing import Any, assert_never

from django.db.models import Exists, OuterRef, Q
from django.db.models.functions import Now
from django.db.models.query import QuerySet
from api.db.models.comment import Comment
from api.db.models.media import Video, Music, Blog, Comic, Picture, Chat
from api.db.models.message import Message
from api.db.models.notification import Notification
from api.db.models.users import Follow
from api.src.domain.entity.notification._convert import convert_data, get_media_model, marshal_data
from api.src.domain.entity.index import get_save_new_ids, sort_ids
from api.src.domain.interface.notification.data import NotificationData
from api.src.domain.interface.notification.interface import FilterOption, NotificationInterface, SortOption
from api.utils.common.result import FatalError, Result
from api.utils.enum.media import MediaType
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo


NOTIFICATION_FIELDS = ["user_from_id", "user_to_id", "type_no", "type_name", "object_id", "object_type"]


def get_comment_media_ulids(comments: list[Comment]) -> dict[int, str]:
    groups: dict[MediaType, list[int]] = {}
    for c in comments:
        groups.setdefault(MediaType(c.type_name), []).append(c.object_id)

    media_ulids: dict[str, str] = {}
    for media_type, media_ids in groups.items():
        model = get_media_model(media_type)
        media_ulids.update({f"{media_type.value}:{obj_id}": str(obj_ulid) for obj_id, obj_ulid in model.objects.filter(id__in=media_ids).values_list("id", "ulid")})

    comment_media_ulids: dict[int, str] = {}
    for c in comments:
        media_ulid = media_ulids.get(f"{c.type_name}:{c.object_id}")
        if media_ulid is not None:
            comment_media_ulids[c.id] = media_ulid
    return comment_media_ulids


class NotificationRepository(NotificationInterface):
    def queryset(self) -> QuerySet[Notification]:
        return Notification.objects.select_related("user_from", "user_to")

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.type_no is not None:
            q_list.append(Q(type_no=filter.type_no))
        if filter.object_type is not None:
            q_list.append(Q(object_type=filter.object_type))
        if filter.object_ids:
            q_list.append(Q(object_id__in=filter.object_ids))
        if filter.user_to_id:
            q_list.append(Q(user_to_id=filter.user_to_id))
        if filter.receiver_id:
            following = Follow.objects.filter(follower_id=filter.receiver_id, following_id=OuterRef("user_from_id"), is_follow=True, created__lt=OuterRef("created"))
            q_list.append(Q(user_to_id=filter.receiver_id) | Q(Exists(following), user_to__isnull=True))
        if filter.enabled_types:
            q_list.append(Q(type_no__in=filter.enabled_types))
        if filter.confirmed_user_id:
            q_list.append(Q(confirmed=filter.confirmed_user_id))
        if filter.exclude_user_id:
            q_list.append(~Q(deleted=filter.exclude_user_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Notification.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[NotificationData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)

        groups: dict[NotificationObjectType, list[int]] = {}
        for n in sorted_objs:
            groups.setdefault(NotificationObjectType(n.object_type), []).append(n.object_id)

        content_map: dict[str, Any] = {}
        comment_media_ulids: dict[int, str] = {}
        for object_type, obj_ids in groups.items():
            match object_type:
                case NotificationObjectType.VIDEO:
                    content_map.update({f"{object_type.value}:{o.id}": o for o in Video.objects.filter(id__in=obj_ids, publish_at__lte=Now())})
                case NotificationObjectType.MUSIC:
                    content_map.update({f"{object_type.value}:{o.id}": o for o in Music.objects.filter(id__in=obj_ids, publish_at__lte=Now())})
                case NotificationObjectType.BLOG:
                    content_map.update({f"{object_type.value}:{o.id}": o for o in Blog.objects.filter(id__in=obj_ids, publish_at__lte=Now())})
                case NotificationObjectType.COMIC:
                    content_map.update({f"{object_type.value}:{o.id}": o for o in Comic.objects.filter(id__in=obj_ids, publish_at__lte=Now())})
                case NotificationObjectType.PICTURE:
                    content_map.update({f"{object_type.value}:{o.id}": o for o in Picture.objects.filter(id__in=obj_ids, publish_at__lte=Now())})
                case NotificationObjectType.CHAT:
                    content_map.update({f"{object_type.value}:{o.id}": o for o in Chat.objects.filter(id__in=obj_ids, publish_at__lte=Now())})
                case NotificationObjectType.FOLLOW:
                    content_map.update({f"{object_type.value}:{o.id}": o for o in Follow.objects.filter(id__in=obj_ids)})
                case NotificationObjectType.COMMENT:
                    comments = list(Comment.objects.filter(id__in=obj_ids, deleted=False))
                    comment_media_ulids.update(get_comment_media_ulids(comments))
                    content_map.update({f"{object_type.value}:{o.id}": o for o in comments if o.id in comment_media_ulids})
                case NotificationObjectType.MESSAGE:
                    content_map.update({f"{object_type.value}:{o.id}": o for o in Message.objects.filter(id__in=obj_ids)})
                case _:
                    assert_never(object_type)

        return Result.ok([
            convert_data(obj, content_map.get(f"{obj.object_type}:{obj.object_id}"), comment_media_ulids)
            for obj in sorted_objs
        ])

    @Result.shield_exception()
    def bulk_save(self, objs: list[NotificationData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, NOTIFICATION_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        if len(ids) == 0:
            return Result.ok(None)
        Notification.objects.filter(id__in=ids).delete()
        return Result.ok(None)

    @Result.shield_exception()
    def delete(self, type_no: NotificationTypeNo, object_type: NotificationObjectType, object_id: int, user_from_id: int) -> Result[None, FatalError]:
        Notification.objects.filter(type_no=type_no, object_type=object_type, object_id=object_id, user_from_id=user_from_id).delete()
        return Result.ok(None)

    @Result.shield_exception()
    def delete_by_user(self, ulid: str, user_id: int) -> Result[None, FatalError]:
        notification = Notification.objects.filter(ulid=ulid).first()
        if notification is None:
            return Result.ok(None)
        notification.confirmed.add(user_id)
        notification.deleted.add(user_id)
        return Result.ok(None)

    @Result.shield_exception()
    def confirm(self, ulid: str, user_id: int) -> Result[None, FatalError]:
        notification = Notification.objects.filter(ulid=ulid).first()
        if notification is None:
            return Result.ok(None)
        notification.confirmed.add(user_id)
        return Result.ok(None)
