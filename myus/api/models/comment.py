from django.db import models
from django.db.models import Count
from django_ulid.models import ulid
from api.models.user import User


class CommentManager(models.Manager):
    def get_queryset(self):
        qs = super(CommentManager,self).get_queryset().annotate(reply_count=Count("reply"))
        return qs.select_related("author", "parent").prefetch_related("like")


class Comment(models.Model):
    """Comment"""
    id        = models.BigAutoField(primary_key=True)
    ulid      = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    author    = models.ForeignKey(User, on_delete=models.CASCADE)
    parent    = models.ForeignKey("self", on_delete=models.CASCADE, related_name="reply", blank=True, null=True)
    type_no   = models.IntegerField()
    type_name = models.CharField(max_length=7, blank=True)
    object_id = models.PositiveIntegerField()
    text      = models.TextField()
    like      = models.ManyToManyField(User, related_name="comment_like", blank=True)
    deleted   = models.BooleanField(default=False)
    created   = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    def __str__(self):
        return str(self.id)

    def total_like(self):
        return self.like.count()
    total_like.short_description = "like"

    def reply_count(self):
        return self.reply.filter(parent=self).count()
    reply_count.short_description = "reply"

    class Meta:
        db_table = "comment"
        verbose_name_plural = "13 コメント"
        indexes = [
            models.Index(fields=["parent"], name="comment_parent_idx"),
            models.Index(fields=["type_no", "object_id"], name="comment_type_object_idx"),
        ]
