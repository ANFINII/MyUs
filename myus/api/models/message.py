from django.db import models
from django.db.models import Count
from django_quill.fields import QuillField
from myus.api.models.user import User
from myus.api.models.media import Chat


class MessageManager(models.Manager):
    def get_queryset(self):
        qs = super(MessageManager,self).get_queryset().annotate(reply_count=Count('reply'))
        return qs.select_related('author', 'parent', 'chat')


class Message(models.Model):
    """Message"""
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    chat    = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='message')
    parent  = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply', blank=True, null=True)
    text    = models.TextField()
    delta   = QuillField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = MessageManager()

    def __str__(self):
        return str(self.id)

    def reply_count(self):
       return self.reply.filter(parent=self).count()
    reply_count.short_description = 'reply'

    class Meta:
        db_table = 'message'
        verbose_name_plural = '14 メッセージ'
        indexes = [models.Index(fields=['parent'], name='message_parent_idx')]
