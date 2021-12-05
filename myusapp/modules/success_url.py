from django.contrib.auth import get_user_model
from django.urls import reverse
from myusapp.models import NotificationModel

User = get_user_model()

def success_url(self, myus_detail, type_no):
    obj = self.object
    user = self.request.user
    NotificationModel.objects.create(
        user_from=user,
        type_no=type_no,
        content_object=obj,
    )
    return reverse(myus_detail, kwargs={'pk': self.object.pk, 'title': self.object.title})
