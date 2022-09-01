from datetime import datetime, timezone, timedelta
from apps.myus.models import Notification, AccessLog
from apps.myus.modules.contains import NotificationTypeNo, models_dict


def get_client_ip(request):
    X_FORWARDED_FOR = request.META.get('HTTP_X_FORWARDED_FOR')
    REMOTE_ADDR = request.META.get('REMOTE_ADDR')
    return X_FORWARDED_FOR.split(',')[0] if X_FORWARDED_FOR else REMOTE_ADDR


def get_detail(self, request):
    self.object = self.get_object()
    obj = self.object
    obj_class = obj.__class__
    obj_name = obj_class.__name__
    ip = get_client_ip(request)
    access_log = AccessLog.objects.filter(ip_address=ip, type=obj_name, type_id=obj.id).first()
    JST = timezone(timedelta(hours=9), 'JST')
    if access_log:
        if datetime.now(JST) - access_log.updated > timedelta(hours=2):
            obj.read += 1
            obj.save(update_fields=['read'])
            access_log.save(update_fields=['updated'])
    else:
        AccessLog.objects.create(ip_address=ip, type=obj_name, type_id=obj.id)
        obj.read += 1
        obj.save(update_fields=['read'])
    author = obj.author
    context = self.get_context_data(object=obj)
    if obj.read == 10000:
        if author.notificationsetting.is_views:
            type_name = [value for key, value in models_dict.items() if obj_class == key][0]
            Notification.objects.create(
                user_from=author,
                user_to=author,
                type_no=NotificationTypeNo.views,
                type_name=type_name,
                content_object=obj,
            )
    if obj.read in (100000, 1000000, 10000000, 100000000, 1000000000):
        notification_obj = Notification.objects.get_or_create(
            user_from=author,
            user_to=author,
            type_no=NotificationTypeNo.views,
            type_name=type_name,
            content_object=obj,
        )
        if notification_obj.confirmed.filter(id=author.id).exists():
            notification_obj.confirmed.remove(author)
        if notification_obj.deleted.filter(id=author.id).exists():
            notification_obj.deleted.remove(author)
    return self.render_to_response(context)
