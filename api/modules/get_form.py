from django.shortcuts import get_object_or_404
from api.models import Notification
from api.modules.contains import NotificationTypeNo, models_dict


def get_detail(self):
    self.object = self.get_object()
    obj = self.object
    obj.read += 1
    obj.save(update_fields=['read'])
    obj_class = obj.__class__
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
