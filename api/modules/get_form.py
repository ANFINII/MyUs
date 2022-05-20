from django.shortcuts import get_object_or_404
from api.models import Notification
from api.modules import contains


def get_detail(self):
    self.object = self.get_object()
    obj = self.object
    obj_class = obj.__class__
    obj_class.objects.filter(id=obj.id).update(read=obj.read + 1)
    context = self.get_context_data(object=obj)
    if obj.read == 10000:
        type_name = [value for key, value in contains.models_dict.items() if obj_class == key]
        Notification.objects.create(
            user_from_id=obj.author.id,
            user_to_id=obj.author.id,
            type_no=contains.notification_type_no['views'],
            type_name=type_name,
            content_object=obj,
        )
    if obj.read in (100000, 1000000, 10000000, 100000000, 1000000000):
        notification_obj = get_object_or_404(Notification, type_no=contains.notification_type_no['views'], object_id=obj.id)
        if notification_obj.confirmed.filter(id=obj.author.id).exists():
            notification_obj.confirmed.remove(obj.author)
        if notification_obj.deleted.filter(id=obj.author.id).exists():
            notification_obj.deleted.remove(obj.author)
    return self.render_to_response(context)
