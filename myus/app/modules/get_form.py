from datetime import datetime, timezone, timedelta
from api.models import Notification, AccessLog
from api.utils.constant import model_dict
from api.utils.enum.index import NotificationTypeNo, NotificationObjectType


def get_client_ip(request):
    X_FORWARDED_FOR = request.META.get("HTTP_X_FORWARDED_FOR")
    REMOTE_ADDR = request.META.get("REMOTE_ADDR")
    return X_FORWARDED_FOR.split(",")[0] if X_FORWARDED_FOR else REMOTE_ADDR


def get_detail(self, request):
    self.object = self.get_object()
    obj = self.object
    obj_class = obj.__class__
    obj_name = obj_class.__name__
    author = obj.author

    ip = get_client_ip(request)
    JST = timezone(timedelta(hours=9), "JST")
    access_log = AccessLog.objects.filter(ip_address=ip, type=obj_name, type_id=obj.id).first()
    if access_log and datetime.now(JST) - access_log.updated > timedelta(hours=2):
        obj.read += 1
        obj.save(update_fields=["read"])
        access_log.save(update_fields=["updated"])
    else:
        AccessLog.objects.create(ip_address=ip, type=obj_name, type_id=obj.id)
        obj.read += 1
        obj.save(update_fields=["read"])

    if obj.read == 10000:
        if author.usernotification.is_views:
            type_name = [value for key, value in model_dict.items() if obj_class == key][0]
            Notification.objects.create(
                user_from=author,
                user_to=author,
                type_no=NotificationTypeNo.VIEWS,
                type_name=type_name,
                object_id=obj.id,
                object_type=NotificationObjectType[obj.__class__.__name__],
            )

    if obj.read in (100000, 1000000, 10000000, 100000000, 1000000000):
        notification_obj = Notification.objects.get_or_create(
            user_from=author,
            user_to=author,
            type_no=NotificationTypeNo.VIEWS,
            type_name=type_name,
            object_id=obj.id,
        )
        if notification_obj.confirmed.filter(id=author.id).exists():
            notification_obj.confirmed.remove(author)
        if notification_obj.deleted.filter(id=author.id).exists():
            notification_obj.deleted.remove(author)

    context = self.get_context_data(object=obj)
    return self.render_to_response(context)
