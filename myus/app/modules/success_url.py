from django.contrib.auth import get_user_model
from django.urls import reverse
from api.models import Notification


User = get_user_model()

def success_url(self, myus_detail, type_no, type_name):
    obj = self.object
    user = self.request.user
    Notification.objects.create(
        user_from=user,
        type_no=type_no,
        type_name=type_name,
        content_object=obj,
    )
    if "app:chat_detail" in str(myus_detail):
        return reverse(myus_detail, kwargs={"pk": self.object.pk,})
    else:
        return reverse(myus_detail, kwargs={"pk": self.object.pk, "title": self.object.title})
