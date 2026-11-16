from django_ulid.models import ulid
from django.db import models
from myus.utils.constants.choice import MEDIA_TYPE_CHOICES
from .channel import Channel


class Series(models.Model):
    """Series"""
    id         = models.BigAutoField(primary_key=True)
    ulid       = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    channel    = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="series")
    media_type = models.CharField(max_length=7, choices=MEDIA_TYPE_CHOICES)
    title      = models.CharField(max_length=100)
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "series"
        verbose_name_plural = "07 Series"
        indexes = [models.Index(fields=["channel", "media_type"], name="series_channel_type_idx")]


class SeriesMedia(models.Model):
    """SeriesMedia"""
    id         = models.BigAutoField(primary_key=True)
    series     = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="series_media")
    media_type = models.CharField(max_length=7, choices=MEDIA_TYPE_CHOICES)
    object_id  = models.PositiveBigIntegerField()
    sequence   = models.IntegerField()

    class Meta:
        db_table = "series_media"
        verbose_name_plural = "07 SeriesMedia"
        constraints = [models.UniqueConstraint(fields=["media_type", "object_id"], name="series_media_object_uniq")]
        indexes = [models.Index(fields=["series", "sequence"], name="series_media_seq_idx")]
