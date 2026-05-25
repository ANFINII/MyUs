from api.utils.enum.i18n import Currency
from api.utils.enum.payment import PaymentProvider, SubscriptionStatus, PaymentStatus, WebhookEventType, WebhookDeliveryStatus
from api.utils.enum.user import GenderType, PlanName, PlanAction


GENDER_CHOICES = ((GenderType.MALE, "男性"), (GenderType.FEMALE, "女性"), (GenderType.SECRET, "秘密"))
ADVERTISE_TYPE_CHOICES = (("all", "全体"), ("one", "個別"))

PLAN_CHOICES = [(p, p) for p in PlanName]
PLAN_ACTION_CHOICES = [(a, a) for a in PlanAction]
CURRENCY_CHOICES = [(c, c) for c in Currency]
PROVIDER_CHOICES = [(p, p) for p in PaymentProvider]
PAYMENT_STATUS_CHOICES = [(s, s) for s in PaymentStatus]
SUBSCRIPTION_STATUS_CHOICES = [(s, s) for s in SubscriptionStatus]
WEBHOOK_EVENT_TYPE_CHOICES = [(t, t) for t in WebhookEventType]
WEBHOOK_DELIVERY_STATUS_CHOICES = [(s, s) for s in WebhookDeliveryStatus]
