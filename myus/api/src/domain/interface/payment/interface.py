from abc import ABC, abstractmethod
from api.src.domain.interface.payment.data import CheckoutData, CheckoutResult


class PaymentInterface(ABC):
    @abstractmethod
    def create_checkout(self, input: CheckoutData) -> CheckoutResult:
        ...
