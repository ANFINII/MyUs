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


class SubscriptionStatus(str, Enum):
    ACTIVE = "Active"
    PAST_DUE = "PastDue"
    CANCELED = "Canceled"
    EXPIRED = "Expired"
    INCOMPLETE = "Incomplete"


class PaymentStatus(str, Enum):
    PENDING = "Pending"
    AUTHORIZED = "Authorized"
    CAPTURED = "Captured"
    FAILED = "Failed"
    REFUNDED = "Refunded"
    CANCELED = "Canceled"
