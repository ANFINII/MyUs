from dataclasses import dataclass
from datetime import datetime
from api.src.domain.interface.payment.data import Money
from api.src.domain.interface.webhook.inbox.data import WebhookInboxData
from api.utils.enum.i18n import Locale
from api.utils.enum.payment import CancelError, CheckoutError, PaymentProvider, PaymentType, SubscriptionStatus, WebhookVerifyError


@dataclass(frozen=True, slots=True)
class MarketplaceData:
    seller_id: str
    application_fee: Money


@dataclass(frozen=True, slots=True)
class CustomerData:
    user_ulid: str
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
class WebhookVerified:
    event: WebhookInboxData


@dataclass(frozen=True, slots=True)
class WebhookVerifyFailed:
    error: WebhookVerifyError
    message: str


type WebhookVerifyResult = WebhookVerified | WebhookVerifyFailed


@dataclass(frozen=True, slots=True)
class CancelSuccess:
    canceled_at: datetime
    period_end: datetime


@dataclass(frozen=True, slots=True)
class CancelFailed:
    error: CancelError
    message: str


type CancelResult = CancelSuccess | CancelFailed


@dataclass(frozen=True, slots=True)
class ProviderSubscriptionData:
    provider: PaymentProvider
    external_id: str
    customer_id: str
    user_ulid: str
    product_code: str
    price: Money
    status: SubscriptionStatus
    started_at: datetime
    current_period_end: datetime
    canceled_at: datetime
