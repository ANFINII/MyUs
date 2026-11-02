from api.src.domain.interface.payment.provider.interface import PaymentInterface
from api.src.injectors.container import injector
from api.utils.enum.payment import PaymentProvider


def get_payment_repository(provider: PaymentProvider) -> PaymentInterface:
    providers = injector.get(dict[PaymentProvider, PaymentInterface])
    return providers[provider]


def included_tax(amount: int, rate: int) -> int:
    tax = abs(amount) * rate // (100 + rate)
    return tax if amount >= 0 else -tax
