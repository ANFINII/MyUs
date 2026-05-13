from enum import Enum


class PaymentProvider(str, Enum):
    STRIPE = "Stripe"


class PaymentType(str, Enum):
    SUBSCRIPTION = "Subscription"
    ONE_TIME = "OneTime"


class CheckoutError(str, Enum):
    UNKNOWN_PRODUCT = "UnknownProduct"
    INVALID_AMOUNT = "InvalidAmount"
    PROVIDER_REJECTED = "ProviderRejected"
    NETWORK_ERROR = "NetworkError"
