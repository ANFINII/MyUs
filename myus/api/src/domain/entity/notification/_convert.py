from api.db.models.notification import Notification
from api.src.domain.interface.notification.data import NotificationData


def convert_data(obj: Notification) -> NotificationData:
    return NotificationData(
        id=obj.id,
        user_from_id=obj.user_from_id,
        user_to_id=obj.user_to_id or 0,
        type_no=obj.type_no,
        type_name=obj.type_name,
        object_id=obj.object_id,
        object_type=obj.object_type,
    )


def marshal_notification(data: NotificationData) -> Notification:
    return Notification(
        id=data.id if data.id != 0 else None,
        user_from_id=data.user_from_id,
        user_to_id=data.user_to_id,
        type_no=data.type_no,
        type_name=data.type_name,
        object_id=data.object_id,
        object_type=data.object_type,
    )
