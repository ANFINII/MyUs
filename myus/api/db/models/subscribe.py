from django.db import models
from api.db.models.channel import Channel
from api.db.models.user import User


class Subscribe(models.Model):
    """Subscribe"""
    id           = models.BigAutoField(primary_key=True)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    channel      = models.ForeignKey(Channel, on_delete=models.CASCADE)
    is_subscribe = models.BooleanField(default=True)
    created      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} : {self.channel}"

    class Meta:
        db_table = "subscribe"
        verbose_name_plural = "11 チャンネル登録"
        indexes = [
            models.Index(fields=["user"], name="subscribe_user_idx"),
            models.Index(fields=["channel"], name="subscribe_channel_idx"),
            models.Index(fields=["user", "channel"], name="subscribe_user_channel_idx"),
        ]
