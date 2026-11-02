from dataclasses import dataclass
from api.utils.enum.payment import WebhookEventType


@dataclass(frozen=True, slots=True)
class StripeEventTypeMap:
    invoice_paid: WebhookEventType
    invoice_payment_failed: WebhookEventType
    customer_subscription_created: WebhookEventType
    customer_subscription_updated: WebhookEventType
    customer_subscription_deleted: WebhookEventType
    charge_refunded: WebhookEventType
    payout_paid: WebhookEventType


STRIPE_EVENT_TYPE_MAP = StripeEventTypeMap(
    invoice_paid=WebhookEventType.PAYMENT_SUCCEEDED,
    invoice_payment_failed=WebhookEventType.PAYMENT_FAILED,
    customer_subscription_created=WebhookEventType.SUBSCRIPTION_CREATED,
    customer_subscription_updated=WebhookEventType.SUBSCRIPTION_UPDATED,
    customer_subscription_deleted=WebhookEventType.SUBSCRIPTION_CANCELED,
    charge_refunded=WebhookEventType.REFUND_ISSUED,
    payout_paid=WebhookEventType.PAYOUT_PAID,
)


def stripe_event_type(event_type: str) -> WebhookEventType | None:
    key = event_type.replace(".", "_")
    return getattr(STRIPE_EVENT_TYPE_MAP, key, None)
