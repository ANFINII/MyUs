from dataclasses import dataclass
from datetime import datetime
from myus.utils.enum.i18n import Country, Locale
from myus.utils.enum.payment import CancelError, CheckoutError, PaymentMethodSessionError, PaymentProvider, PaymentType, PlanChangeError, RevokeError, SellerOnboardError, SellerStatusError, WebhookVerifyError
from ..data import Money
from ..event.data import PaymentEventData, ProviderSubscriptionData


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
    event: PaymentEventData


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
class RevokeSuccess:
    subscription: ProviderSubscriptionData


@dataclass(frozen=True, slots=True)
class RevokeFailed:
    error: RevokeError
    message: str


type RevokeResult = RevokeSuccess | RevokeFailed


@dataclass(frozen=True, slots=True)
class PlanChangeSuccess:
    subscription: ProviderSubscriptionData


@dataclass(frozen=True, slots=True)
class PlanChangeFailed:
    error: PlanChangeError
    message: str


type PlanChangeResult = PlanChangeSuccess | PlanChangeFailed


@dataclass(frozen=True, slots=True)
class PaymentMethodSessionCreated:
    redirect_url: str


@dataclass(frozen=True, slots=True)
class PaymentMethodSessionFailed:
    error: PaymentMethodSessionError
    message: str


type PaymentMethodSessionResult = PaymentMethodSessionCreated | PaymentMethodSessionFailed


@dataclass(frozen=True, slots=True)
class SellerOnboard:
    external_id: str
    user_ulid: str
    email: str
    country: Country
    return_url: str
    refresh_url: str


@dataclass(frozen=True, slots=True)
class SellerOnboardCreated:
    external_id: str
    redirect_url: str


@dataclass(frozen=True, slots=True)
class SellerOnboardFailed:
    error: SellerOnboardError
    message: str


type SellerOnboardResult = SellerOnboardCreated | SellerOnboardFailed


@dataclass(frozen=True, slots=True)
class SellerStatusSuccess:
    is_enabled: bool


@dataclass(frozen=True, slots=True)
class SellerStatusFailed:
    error: SellerStatusError
    message: str


type SellerStatusResult = SellerStatusSuccess | SellerStatusFailed
