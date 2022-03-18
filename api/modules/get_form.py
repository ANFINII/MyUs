from django.shortcuts import get_object_or_404
from api.models import Notification
from api.models import Video, Live, Music, Picture, Blog, Chat, Collabo

def get_detail(self):
    self.object = self.get_object()
    self.object.read += 1
    self.object.save()
    context = self.get_context_data(object=self.object)
    if self.object.read == 10000:
        type_name = ''
        if self.object.__class__ == Video:
            type_name = 'video'
        if self.object.__class__ == Live:
            type_name = 'live'
        if self.object.__class__ == Music:
            type_name = 'music'
        if self.object.__class__ == Picture:
            type_name = 'picture'
        if self.object.__class__ == Blog:
            type_name = 'blog'
        if self.object.__class__ == Chat:
            type_name = 'chat'
        if self.object.__class__ == Collabo:
            type_name = 'collabo'
        Notification.objects.create(
            user_from_id=self.object.author.id,
            user_to_id=self.object.author.id,
            type_no=11,
            type_name=type_name,
            content_object=self.object,
        )
    if self.object.read in (100000, 1000000, 10000000, 100000000, 1000000000):
        notification_obj = get_object_or_404(Notification, type_no=11, object_id=self.object.id)
        if notification_obj.confirmed.filter(id=self.object.author.id).exists():
            notification_obj.confirmed.remove(self.object.author)
        if notification_obj.deleted.filter(id=self.object.author.id).exists():
            notification_obj.deleted.remove(self.object.author)
    return self.render_to_response(context)
