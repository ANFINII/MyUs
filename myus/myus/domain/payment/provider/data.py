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
class RedirectUrlsData:
    success_url: str
    cancel_url: str


@dataclass(frozen=True, slots=True)
class CheckoutData:
    product_code: str
    description: str
    price: Money
    payment_type: PaymentType
    customer: CustomerData
    redirect: RedirectUrlsData
    marketplace: MarketplaceData
    locale: Locale


@dataclass(frozen=True, slots=True)
class CheckoutSessionData:
    provider: PaymentProvider
    external_id: str
    redirect_url: str


@dataclass(frozen=True, slots=True)
class CheckoutCreatedData:
    session: CheckoutSessionData


@dataclass(frozen=True, slots=True)
class CheckoutFailedData:
    error: CheckoutError
    message: str


type CheckoutResult = CheckoutCreatedData | CheckoutFailedData


@dataclass(frozen=True, slots=True)
class WebhookVerifiedData:
    event: PaymentEventData


@dataclass(frozen=True, slots=True)
class WebhookVerifyFailedData:
    error: WebhookVerifyError
    message: str


type WebhookVerifyResult = WebhookVerifiedData | WebhookVerifyFailedData


@dataclass(frozen=True, slots=True)
class CancelSuccessData:
    canceled_at: datetime
    period_end: datetime


@dataclass(frozen=True, slots=True)
class CancelFailedData:
    error: CancelError
    message: str


type CancelResult = CancelSuccessData | CancelFailedData


@dataclass(frozen=True, slots=True)
class RevokeSuccessData:
    subscription: ProviderSubscriptionData


@dataclass(frozen=True, slots=True)
class RevokeFailedData:
    error: RevokeError
    message: str


type RevokeResult = RevokeSuccessData | RevokeFailedData


@dataclass(frozen=True, slots=True)
class PlanChangeSuccessData:
    subscription: ProviderSubscriptionData


@dataclass(frozen=True, slots=True)
class PlanChangeFailedData:
    error: PlanChangeError
    message: str


type PlanChangeResult = PlanChangeSuccessData | PlanChangeFailedData


@dataclass(frozen=True, slots=True)
class PaymentMethodSessionCreatedData:
    redirect_url: str


@dataclass(frozen=True, slots=True)
class PaymentMethodSessionFailedData:
    error: PaymentMethodSessionError
    message: str


type PaymentMethodSessionResult = PaymentMethodSessionCreatedData | PaymentMethodSessionFailedData


@dataclass(frozen=True, slots=True)
class SellerOnboardData:
    external_id: str
    user_ulid: str
    email: str
    country: Country
    return_url: str
    refresh_url: str


@dataclass(frozen=True, slots=True)
class SellerOnboardCreatedData:
    external_id: str
    redirect_url: str


@dataclass(frozen=True, slots=True)
class SellerOnboardFailedData:
    error: SellerOnboardError
    message: str


type SellerOnboardResult = SellerOnboardCreatedData | SellerOnboardFailedData


@dataclass(frozen=True, slots=True)
class SellerStatusSuccessData:
    is_enabled: bool


@dataclass(frozen=True, slots=True)
class SellerStatusFailedData:
    error: SellerStatusError
    message: str


type SellerStatusResult = SellerStatusSuccessData | SellerStatusFailedData
