import datetime
from django.db import models
from api.db.models.user import User
from api.utils.constants.choice import CURRENCY_CHOICES, PROVIDER_CHOICES, PAYMENT_STATUS_CHOICES, LEDGER_ENTRY_TYPE_CHOICES, PAYOUT_STATUS_CHOICES, SUBSCRIPTION_STATUS_CHOICES, WEBHOOK_EVENT_TYPE_CHOICES
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import SubscriptionStatus, PaymentStatus, PayoutStatus

DATETIME_MIN = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)


class PaymentEvent(models.Model):
    """PaymentEvent"""
    id           = models.BigAutoField(primary_key=True)
    provider     = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    event_id     = models.CharField(max_length=255)
    event_type   = models.CharField(max_length=30, choices=WEBHOOK_EVENT_TYPE_CHOICES)
    external_id  = models.CharField(max_length=255)
    payload      = models.TextField(blank=True)
    content      = models.TextField(blank=True)
    occurred_at  = models.DateTimeField(default=DATETIME_MIN)
    processed_at = models.DateTimeField(default=DATETIME_MIN)
    attempts     = models.PositiveIntegerField(default=0)
    last_error   = models.TextField(blank=True)
    created      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider}:{self.event_id}:{self.event_type}"

    class Meta:
        db_table = "payment_event"
        verbose_name_plural = "001 PaymentEvent"
        constraints = [
            models.UniqueConstraint(fields=["provider", "event_id"], name="payment_event_provider_event_id_uniq"),
        ]
        indexes = [
            models.Index(fields=["external_id", "occurred_at"], name="payment_event_external_idx"),
            models.Index(fields=["processed_at", "occurred_at"], name="payment_event_processed_idx"),
        ]


class PaymentCustomer(models.Model):
    """PaymentCustomer"""
    id          = models.BigAutoField(primary_key=True)
    user        = models.ForeignKey(User, on_delete=models.PROTECT, related_name="payment_customers")
    provider    = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    external_id = models.CharField(max_length=255)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id}:{self.provider}:{self.external_id}"

    class Meta:
        db_table = "payment_customer"
        verbose_name_plural = "001 PaymentCustomer"
        constraints = [
            models.UniqueConstraint(fields=["provider", "external_id"], name="payment_customer_provider_external_uniq"),
            models.UniqueConstraint(fields=["user", "provider"], name="payment_customer_user_provider_uniq"),
        ]


class Subscription(models.Model):
    """Subscription"""
    id                 = models.BigAutoField(primary_key=True)
    payment_customer   = models.ForeignKey(PaymentCustomer, on_delete=models.PROTECT, related_name="subscriptions")
    seller_id          = models.CharField(max_length=26, blank=True)
    external_id        = models.CharField(max_length=255)
    product_code       = models.CharField(max_length=30)
    price_amount       = models.IntegerField(default=0)
    price_currency     = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=Currency.JPY)
    status             = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS_CHOICES, default=SubscriptionStatus.INCOMPLETE)
    started_at         = models.DateTimeField(default=DATETIME_MIN)
    current_period_end = models.DateTimeField(default=DATETIME_MIN)
    canceled_at        = models.DateTimeField(default=DATETIME_MIN)
    last_event_at      = models.DateTimeField(default=DATETIME_MIN)

    def __str__(self):
        return f"{self.payment_customer_id}:{self.product_code}:{self.status}"

    class Meta:
        db_table = "subscription"
        verbose_name_plural = "001 Subscription"
        constraints = [
            models.UniqueConstraint(fields=["payment_customer", "external_id"], name="subscription_customer_external_uniq"),
        ]
        indexes = [
            models.Index(fields=["external_id"], name="subscription_external_idx"),
        ]


class PaymentTransaction(models.Model):
    """PaymentTransaction"""
    id               = models.BigAutoField(primary_key=True)
    payment_customer = models.ForeignKey(PaymentCustomer, on_delete=models.PROTECT, related_name="payment_transactions")
    subscription     = models.ForeignKey(Subscription, on_delete=models.PROTECT, related_name="payment_transactions", null=True, blank=True)
    external_id      = models.CharField(max_length=255)
    currency         = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=Currency.JPY)
    tax_rate         = models.IntegerField(default=0)
    receipt_number   = models.CharField(max_length=30, blank=True)
    status           = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PaymentStatus.PENDING)
    paid_at          = models.DateTimeField(default=DATETIME_MIN)
    last_event_at    = models.DateTimeField(default=DATETIME_MIN)

    def __str__(self):
        return f"{self.payment_customer_id}:{self.external_id}:{self.status}"

    class Meta:
        db_table = "payment_transaction"
        verbose_name_plural = "001 PaymentTransaction"
        constraints = [
            models.UniqueConstraint(fields=["payment_customer", "external_id"], name="payment_transaction_customer_external_uniq"),
        ]
        indexes = [
            models.Index(fields=["external_id"], name="payment_tx_external_idx"),
            models.Index(fields=["paid_at"], name="payment_tx_paid_idx"),
        ]


class PaymentPayout(models.Model):
    """PaymentPayout"""
    id            = models.BigAutoField(primary_key=True)
    provider      = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    external_id   = models.CharField(max_length=255)
    amount        = models.IntegerField(default=0)
    currency      = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=Currency.JPY)
    status        = models.CharField(max_length=20, choices=PAYOUT_STATUS_CHOICES, default=PayoutStatus.PENDING)
    arrival_at    = models.DateTimeField(default=DATETIME_MIN)
    last_event_at = models.DateTimeField(default=DATETIME_MIN)

    def __str__(self):
        return f"{self.provider}:{self.external_id}:{self.status}"

    class Meta:
        db_table = "payment_payout"
        verbose_name_plural = "001 PaymentPayout"
        constraints = [
            models.UniqueConstraint(fields=["provider", "external_id"], name="payment_payout_provider_external_uniq"),
        ]
        indexes = [
            models.Index(fields=["arrival_at"], name="payment_payout_arrival_idx"),
        ]


class PaymentLedgerEntry(models.Model):
    """PaymentLedgerEntry"""
    id          = models.BigAutoField(primary_key=True)
    transaction = models.ForeignKey(PaymentTransaction, on_delete=models.PROTECT, related_name="ledger_entries")
    payout      = models.ForeignKey(PaymentPayout, on_delete=models.PROTECT, related_name="ledger_entries", null=True, blank=True)
    event       = models.ForeignKey(PaymentEvent, on_delete=models.PROTECT, related_name="ledger_entries")
    external_id = models.CharField(max_length=255)
    entry_type  = models.CharField(max_length=20, choices=LEDGER_ENTRY_TYPE_CHOICES)
    amount      = models.IntegerField(default=0)
    tax_amount  = models.IntegerField(default=0)
    occurred_at = models.DateTimeField(default=DATETIME_MIN)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id}:{self.entry_type}:{self.amount}"

    class Meta:
        db_table = "payment_ledger_entry"
        verbose_name_plural = "001 PaymentLedgerEntry"
        constraints = [
            models.UniqueConstraint(fields=["transaction", "external_id", "entry_type"], name="payment_ledger_transaction_external_type_uniq"),
        ]
        indexes = [
            models.Index(fields=["occurred_at"], name="payment_ledger_occurred_idx"),
        ]
