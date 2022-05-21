from django.shortcuts import get_object_or_404
from api.models import Notification
from api.modules import contains


def get_detail(self):
    self.object = self.get_object()
    obj = self.object
    obj.read += 1
    obj.save(update_fields=['read'])
    obj_class = obj.__class__
    context = self.get_context_data(object=obj)
    if obj.read == 10000:
        type_name = [value for key, value in contains.models_dict.items() if obj_class == key][0]
        Notification.objects.create(
            user_from=obj.author,
            user_to=obj.author,
            type_no=contains.notification_type_dict['views'][0],
            type_name=type_name,
            content_object=obj,
        )
    if obj.read in (100000, 1000000, 10000000, 100000000, 1000000000):
        notification_obj = get_object_or_404(Notification, type_no=contains.notification_type_dict['views'][0], object_id=obj.id)
        if notification_obj.confirmed.filter(id=obj.author.id).exists():
            notification_obj.confirmed.remove(obj.author)
        if notification_obj.deleted.filter(id=obj.author.id).exists():
            notification_obj.deleted.remove(obj.author)
    return self.render_to_response(context)
