import datetime
from django.db import models
from api.db.models.user import User
from api.utils.constants.choice import CURRENCY_CHOICES, PROVIDER_CHOICES, PAYMENT_STATUS_CHOICES, SUBSCRIPTION_STATUS_CHOICES, WEBHOOK_EVENT_TYPE_CHOICES
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import SubscriptionStatus, PaymentStatus

DATETIME_MIN = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)


class Subscription(models.Model):
    """Subscription"""
    id                 = models.BigAutoField(primary_key=True)
    customer           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    seller_id          = models.CharField(max_length=26, blank=True)
    provider           = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    external_id        = models.CharField(max_length=255)
    product_code       = models.CharField(max_length=30)
    price_amount       = models.IntegerField(default=0)
    price_currency     = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=Currency.JPY)
    status             = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS_CHOICES, default=SubscriptionStatus.INCOMPLETE)
    started_at         = models.DateTimeField(default=DATETIME_MIN)
    current_period_end = models.DateTimeField(default=DATETIME_MIN)
    canceled_at        = models.DateTimeField(default=DATETIME_MIN)

    def __str__(self):
        return f"{self.customer_id}:{self.product_code}:{self.status}"

    class Meta:
        db_table = "subscription"
        verbose_name_plural = "001 Subscription"
        indexes = [
            models.Index(fields=["customer", "status"], name="subscription_customer_status_idx"),
            models.Index(fields=["provider", "external_id"], name="subscription_external_idx"),
        ]


class PaymentTransaction(models.Model):
    """PaymentTransaction"""
    id              = models.BigAutoField(primary_key=True)
    subscription_id = models.BigIntegerField(default=0)
    customer        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_transactions")
    provider        = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    external_id     = models.CharField(max_length=255)
    price_amount    = models.IntegerField(default=0)
    price_currency  = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=Currency.JPY)
    status          = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PaymentStatus.PENDING)
    paid_at         = models.DateTimeField(default=DATETIME_MIN)

    def __str__(self):
        return f"{self.customer_id}:{self.external_id}:{self.status}"

    class Meta:
        db_table = "payment_transaction"
        verbose_name_plural = "001 PaymentTransaction"
        indexes = [
            models.Index(fields=["customer", "-paid_at"], name="payment_tx_customer_paid_idx"),
            models.Index(fields=["provider", "external_id"], name="payment_tx_external_idx"),
        ]


class WebhookEvent(models.Model):
    """WebhookEvent"""
    id          = models.BigAutoField(primary_key=True)
    provider    = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    event_id    = models.CharField(max_length=255)
    event_type  = models.CharField(max_length=30, choices=WEBHOOK_EVENT_TYPE_CHOICES)
    external_id = models.CharField(max_length=255)
    occurred_at = models.DateTimeField(default=DATETIME_MIN)

    def __str__(self):
        return f"{self.provider}:{self.event_id}:{self.event_type}"

    class Meta:
        db_table = "webhook_event"
        verbose_name_plural = "001 WebhookEvent"
        constraints = [
            models.UniqueConstraint(fields=["provider", "event_id"], name="webhook_event_provider_event_id_uniq"),
        ]
        indexes = [
            models.Index(fields=["external_id"], name="webhook_event_external_idx"),
        ]
