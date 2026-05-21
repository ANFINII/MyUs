from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.payment.webhook_event.data import WebhookEventData
from api.utils.enum.i18n import Currency, Locale
from api.utils.enum.payment import CheckoutError, PaymentProvider, PaymentStatus, PaymentType, SubscriptionStatus, WebhookVerifyError


@dataclass(frozen=True, slots=True)
class Money:
    amount: int
    currency: Currency


@dataclass(frozen=True, slots=True)
class MarketplaceData:
    seller_id: str
    application_fee: Money


@dataclass(frozen=True, slots=True)
class CustomerData:
    email: str


@dataclass(frozen=True, slots=True)
class RedirectUrls:
    success_url: str
    cancel_url: str


@dataclass(frozen=True, slots=True)
class CheckoutData:
    product_code: str
    description: str
    price: Money
    payment_type: PaymentType
    customer: CustomerData
    redirect: RedirectUrls
    marketplace: MarketplaceData
    locale: Locale


@dataclass(frozen=True, slots=True)
class CheckoutSessionData:
    provider: PaymentProvider
    external_id: str
    redirect_url: str


@dataclass(frozen=True, slots=True)
class CheckoutCreated:
    session: CheckoutSessionData


@dataclass(frozen=True, slots=True)
class CheckoutFailed:
    error: CheckoutError
    message: str


type CheckoutResult = CheckoutCreated | CheckoutFailed


@dataclass(frozen=True, slots=True)
class SubscriptionData:
    id: int
    customer_user_id: int
    seller_id: str
    provider: PaymentProvider
    external_id: str
    product_code: str
    price: Money
    status: SubscriptionStatus
    started_at: datetime
    current_period_end: datetime
    canceled_at: datetime


@dataclass(frozen=True, slots=True)
class PaymentTransactionData:
    id: int
    subscription_id: int
    customer_user_id: int
    provider: PaymentProvider
    external_id: str
    price: Money
    status: PaymentStatus
    paid_at: datetime


@dataclass(frozen=True, slots=True)
class WebhookVerified:
    event: WebhookEventData


@dataclass(frozen=True, slots=True)
class WebhookVerifyFailed:
    error: WebhookVerifyError
    message: str


type WebhookVerifyResult = WebhookVerified | WebhookVerifyFailed
