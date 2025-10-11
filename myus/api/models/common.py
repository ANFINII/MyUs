from django.db import models
from django_ulid.models import ulid
from api.models.user import User
from api.utils.functions.file import image_upload, video_upload


class AccessLog(models.Model):
    """AccessLog"""
    id         = models.BigAutoField(primary_key=True)
    ip_address = models.GenericIPAddressField()
    type       = models.CharField(max_length=7, blank=True)
    type_id    = models.BigIntegerField(blank=True, null=True)
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ip_address)

    class Meta:
        db_table = "access_log"
        verbose_name_plural = "002 Access Log"
        indexes = [models.Index(fields=["ip_address", "type", "type_id"], name="ip_address_type_idx")]


class Advertise(models.Model):
    """Advertise"""
    choice  = (("all", "全体"), ("one", "個別"))
    id      = models.BigAutoField(primary_key=True)
    ulid    = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=100)
    url     = models.URLField()
    content = models.TextField()
    image   = models.ImageField(upload_to=image_upload)
    video   = models.FileField(upload_to=video_upload)
    read    = models.IntegerField(default=0)
    type    = models.CharField(choices=choice, max_length=3)
    period  = models.DateField()
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id is None:
            image = self.image
            video  = self.video
            self.image = None
            self.video  = None
            super().save(*args, **kwargs)
            self.image = image
            self.video  = video
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "advertise"
        verbose_name_plural = "12 広告設定"
