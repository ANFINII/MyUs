from django.db import models
from django_ulid.models import ulid
from api.db.models.user import User
from api.utils.functions.file import avatar_upload


class Channel(models.Model):
    """Channel"""
    img         = "../static/img/user_icon.png"
    id          = models.BigAutoField(primary_key=True)
    ulid        = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    avatar      = models.ImageField(upload_to=avatar_upload, default=img, blank=True)
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_default  = models.BooleanField(default=False)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "channel"
        verbose_name_plural = "Channel"
