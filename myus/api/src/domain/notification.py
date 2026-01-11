from api.db.models.notification import Notification
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
    def update(cls, obj: Notification, **kwargs) -> None:
        if not kwargs:
            return

        [set_attr(obj, key, value) for key, value in kwargs.items()]
        obj.save(update_fields=list(kwargs.keys()))
        return

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
