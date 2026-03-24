from typing import Any

from django.utils.html import strip_tags
from django_ulid.models import ulid

from api.db.models.notification import Notification
from api.src.domain.interface.notification.data import NotificationContentData, NotificationData


def convert_data(obj: Notification, content_obj: Any | None) -> NotificationData:
    content = get_content(content_obj)

    return NotificationData(
        id=obj.id,
        ulid=str(obj.ulid),
        user_from_id=obj.user_from_id,
        user_to_id=obj.user_to_id or 0,
        type_no=obj.type_no,
        type_name=obj.type_name,
        object_id=obj.object_id,
        object_type=obj.object_type,
        content=content,
    )


def get_content(obj: Any | None) -> NotificationContentData:
    if obj is None:
        return NotificationContentData(id=0, ulid="", title="", text="", read=0)

    return NotificationContentData(
        id=0,
        ulid=str(getattr(obj, "ulid", "")),
        title=str(getattr(obj, "title", "")),
        text=strip_tags(str(getattr(obj, "text", getattr(obj, "content", "")))),
        read=int(getattr(obj, "read", 0)),
    )


def marshal_data(data: NotificationData) -> Notification:
    return Notification(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        user_from_id=data.user_from_id,
        user_to_id=data.user_to_id,
        type_no=data.type_no,
        type_name=data.type_name,
        object_id=data.object_id,
        object_type=data.object_type,
    )
