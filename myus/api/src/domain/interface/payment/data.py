from dataclasses import dataclass
from api.utils.enum.i18n import Currency, Locale
from api.utils.enum.payment import CheckoutError, PaymentProvider, PaymentType


@dataclass(frozen=True, slots=True)
class Money:
    amount: int
    currency: Currency


@dataclass(frozen=True, slots=True)
class CustomerData:
    email: str


@dataclass(frozen=True, slots=True)
class RedirectUrls:
    success_url: str
    cancel_url: str


@dataclass(frozen=True, slots=True)
class MarketplaceData:
    seller_id: str
    application_fee: Money


@dataclass(frozen=True, slots=True)
class CheckoutData:
    payment_type: PaymentType
    price: Money
    customer: CustomerData
    description: str
    product_ref: str
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
