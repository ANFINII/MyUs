from django.db import models
from api.utils.constants.choice import PROVIDER_CHOICES


class EsEvent(models.Model):
    """EsEvent"""
    id             = models.BigAutoField(primary_key=True)
    event_id       = models.UUIDField(unique=True)
    aggregate_type = models.CharField(max_length=50)
    aggregate_id   = models.CharField(max_length=255)
    seq            = models.PositiveIntegerField()
    event_type     = models.CharField(max_length=100)
    payload        = models.TextField()
    occurred_at    = models.DateTimeField()
    created        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aggregate_type}:{self.aggregate_id}:{self.seq}:{self.event_type}"

    class Meta:
        db_table = "es_event"
        verbose_name_plural = "002 EsEvent"
        constraints = [
            models.UniqueConstraint(fields=["aggregate_type", "aggregate_id", "seq"], name="es_event_aggregate_seq_uniq"),
        ]


class EsOutbox(models.Model):
    """EsOutbox"""
    id             = models.BigAutoField(primary_key=True)
    aggregate_type = models.CharField(max_length=50)
    aggregate_id   = models.CharField(max_length=255)
    seq            = models.PositiveIntegerField()
    created        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aggregate_type}:{self.aggregate_id}:{self.seq}"

    class Meta:
        db_table = "es_outbox"
        verbose_name_plural = "002 EsOutbox"
        constraints = [
            models.UniqueConstraint(fields=["aggregate_type", "aggregate_id", "seq"], name="es_outbox_aggregate_seq_uniq"),
        ]


class EsSubscriptionLookup(models.Model):
    """EsSubscriptionLookup"""
    id           = models.BigAutoField(primary_key=True)
    aggregate_id = models.CharField(max_length=26, unique=True)
    provider     = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    external_id  = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.provider}:{self.external_id}:{self.aggregate_id}"

    class Meta:
        db_table = "es_subscription_lookup"
        verbose_name_plural = "002 EsSubscriptionLookup"
        constraints = [
            models.UniqueConstraint(fields=["provider", "external_id"], name="es_subscription_lookup_external_uniq"),
        ]
