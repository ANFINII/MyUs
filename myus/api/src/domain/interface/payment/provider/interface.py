from abc import ABC, abstractmethod
from api.src.domain.interface.payment.provider.data import CheckoutData, CheckoutResult, WebhookVerifyResult


class PaymentInterface(ABC):
    @abstractmethod
    def create_checkout(self, input: CheckoutData) -> CheckoutResult:
        ...

    @abstractmethod
    def verify_webhook(self, payload: bytes, signature: str) -> WebhookVerifyResult:
        ...
