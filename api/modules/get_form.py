from datetime import datetime, timezone, timedelta
from api.models import Notification, AccessLog
from api.modules.contains import NotificationTypeNo, models_dict


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address


def get_detail(self, request):
    self.object = self.get_object()
    obj = self.object
    obj_class = obj.__class__
    obj_name = obj_class.__name__
    ip_address = get_client_ip(request)
    access_log_obj = AccessLog.objects.filter(ip_address=ip_address, type=obj_name, type_id=obj.id).first()
    JST = timezone(timedelta(hours=9), 'JST')
    if access_log_obj:
        if datetime.now(JST) - access_log_obj.updated > timedelta(hours=2):
            obj.read += 1
            obj.save(update_fields=['read'])
            access_log_obj.save(update_fields=['updated'])
    else:
        AccessLog.objects.create(ip_address=ip_address, type=obj_name, type_id=obj.id)
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
