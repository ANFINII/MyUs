from django.db import models
from django.db.models import Count
from django_quill.fields import QuillField
from django_ulid.models import ulid
from api.db.models.media import Chat
from api.db.models.user import User


class MessageManager(models.Manager):
    def get_queryset(self):
        qs = super(MessageManager,self).get_queryset().annotate(reply_count=Count("reply"))
        return qs.select_related("author", "parent", "chat")


class Message(models.Model):
    """Message"""
    id      = models.BigAutoField(primary_key=True)
    ulid    = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    chat    = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="message")
    parent  = models.ForeignKey("self", on_delete=models.CASCADE, related_name="reply", null=True)
    text    = models.TextField()
    delta   = QuillField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = MessageManager()

    def __str__(self):
        return str(self.id)

    def reply_count(self):
       return self.reply.filter(parent=self).count()
    reply_count.short_description = "reply"

    class Meta:
        db_table = "message"
        verbose_name_plural = "14 メッセージ"
        indexes = [models.Index(fields=["parent"], name="message_parent_idx")]
