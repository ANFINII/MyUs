from abc import ABC, abstractmethod
from api.src.domain.interface.payment.data import CheckoutData, CheckoutResult
from api.utils.enum.payment import PaymentProvider


class PaymentProviderInterface(ABC):
    @abstractmethod
    def kind(self) -> PaymentProvider:
        ...

    @abstractmethod
    def create_checkout(self, input: CheckoutData) -> CheckoutResult:
        ...
