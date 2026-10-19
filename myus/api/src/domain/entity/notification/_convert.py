from typing import Any, assert_never

from django.utils.html import strip_tags
from django_ulid.models import ulid

from api.db.models.media import Video, Music, Blog, Comic, Picture, Chat
from api.db.models.notification import Notification
from api.src.domain.interface.notification.data import NotificationContentData, NotificationData
from api.utils.enum.media import MediaType
from api.utils.enum.notification import NotificationObjectType


def convert_data(obj: Notification, content_obj: Any | None, comment_media_ulids: dict[int, str]) -> NotificationData:
    content = get_content(NotificationObjectType(obj.object_type), content_obj, comment_media_ulids)

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


def get_content(object_type: NotificationObjectType, obj: Any | None, comment_media_ulids: dict[int, str]) -> NotificationContentData | None:
    if obj is None:
        return None

    media_type, media_ulid, thread_ulid = get_link(object_type, obj, comment_media_ulids)
    return NotificationContentData(
        id=0,
        ulid=str(getattr(obj, "ulid", "")),
        title=str(getattr(obj, "title", "")),
        text=strip_tags(str(getattr(obj, "text", getattr(obj, "content", "")))),
        read=int(getattr(obj, "read", 0)),
        media_type=media_type,
        media_ulid=media_ulid,
        thread_ulid=thread_ulid,
    )


def get_link(object_type: NotificationObjectType, obj: Any, comment_media_ulids: dict[int, str]) -> tuple[MediaType | None, str, str]:
    match object_type:
        case NotificationObjectType.VIDEO | NotificationObjectType.MUSIC | NotificationObjectType.BLOG | NotificationObjectType.COMIC | NotificationObjectType.PICTURE | NotificationObjectType.CHAT:
            return MediaType(object_type.value), str(obj.ulid), ""
        case NotificationObjectType.COMMENT:
            return MediaType(obj.type_name), comment_media_ulids[obj.id], ""
        case NotificationObjectType.MESSAGE:
            thread_ulid = obj.parent.ulid if obj.parent_id else obj.ulid
            return MediaType.CHAT, str(obj.chat.ulid), str(thread_ulid)
        case NotificationObjectType.FOLLOW:
            return None, "", ""
        case _:
            assert_never(object_type)


def get_media_model(media_type: MediaType) -> type[Video] | type[Music] | type[Blog] | type[Comic] | type[Picture] | type[Chat]:
    match media_type:
        case MediaType.VIDEO:
            return Video
        case MediaType.MUSIC:
            return Music
        case MediaType.BLOG:
            return Blog
        case MediaType.COMIC:
            return Comic
        case MediaType.PICTURE:
            return Picture
        case MediaType.CHAT:
            return Chat
        case _:
            assert_never(media_type)


def marshal_data(data: NotificationData) -> Notification:
    return Notification(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        user_from_id=data.user_from_id,
        user_to_id=data.user_to_id if data.user_to_id != 0 else None,
        type_no=data.type_no,
        type_name=data.type_name,
        object_id=data.object_id,
        object_type=data.object_type,
    )
