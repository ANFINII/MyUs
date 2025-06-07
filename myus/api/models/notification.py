from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from api.models.user import User


class Notification(models.Model):
    """Notification"""
    user_from = models.ForeignKey(User, related_name="user_from", on_delete=models.CASCADE)
    user_to   = models.ForeignKey(User, related_name="user_to", on_delete=models.CASCADE, blank=True, null=True)
    type_no   = models.IntegerField()
    type_name = models.CharField(max_length=7, blank=True)
    object_id = models.PositiveIntegerField()
    confirmed = models.ManyToManyField(User, related_name="confirmed", blank=True)
    deleted   = models.ManyToManyField(User, related_name="deleted", blank=True)
    created   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content_object)

    def title(self):
        return self.content_object
    title.short_description = "title"

    def confirmed_count(self):
        return self.confirmed.count()
    confirmed_count.short_description = "confirmed"

    def deleted_count(self):
        return self.deleted.count()
    deleted_count.short_description = "deleted"

    class Meta:
        db_table = "notification"
        verbose_name_plural = "11 通知確認"
        indexes = [
            models.Index(fields=["user_from", "user_to"], name="notification_from_to_idx"),
            models.Index(fields=["type_no", "object_id"], name="notification_type_object_idx"),
        ]
