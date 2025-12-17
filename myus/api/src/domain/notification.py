from api.models.notification import Notification
from api.utils.enum.index import NotificationTypeNo
from api.utils.functions.index import set_attr


class NotificationDomain:
    @classmethod
    def get(cls, type_no: NotificationTypeNo, object_id: int) -> Notification | None:
        return Notification.objects.filter(type_no=type_no, object_id=object_id).first()

    @classmethod
    def create(cls, **kwargs) -> Notification:
       return Notification.objects.create(**kwargs)

    @classmethod
    def update(cls, notification: Notification, **kwargs) -> None:
        if not kwargs:
            return

        [set_attr(notification, key, value) for key, value in kwargs.items()]
        Notification.save(update_fields=list[str](kwargs.keys()))

    @classmethod
    def delete(cls, type_no: NotificationTypeNo, object_id: int) -> None:
        notification = Notification.objects.filter(type_no=type_no, object_id=object_id)
        notification.delete()


    #     NotificationData(
    #         id=notification.id,
    #         user_from=notification.user_from,
    #         user_to=notification.user_to,
    #         type_no=notification.type_no,
    #         type_name=notification.type_name,
    #         object_id=notification.object_id,
    #         object_type=notification.object_type,
    #     )
