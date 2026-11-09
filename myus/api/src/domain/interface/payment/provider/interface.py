from abc import ABC, abstractmethod
from api.src.domain.interface.payment.event.data import ProviderSubscriptionData
from api.src.domain.interface.payment.provider.data import CancelResult, CheckoutData, CheckoutResult, PlanChangeResult, RevokeResult, WebhookVerifyResult
from api.utils.common.result import FatalError, Result


class PaymentInterface(ABC):
    @abstractmethod
    def create_checkout(self, input: CheckoutData) -> Result[CheckoutResult, FatalError]:
        ...

    @abstractmethod
    def verify_webhook(self, payload: bytes, signature: str) -> Result[WebhookVerifyResult, FatalError]:
        ...

    @abstractmethod
    def cancel_subscription(self, external_id: str, idempotency_key: str) -> Result[CancelResult, FatalError]:
        ...

    @abstractmethod
    def revoke_cancellation(self, external_id: str) -> Result[RevokeResult, FatalError]:
        ...

    @abstractmethod
    def change_plan(self, external_id: str, product_code: str) -> Result[PlanChangeResult, FatalError]:
        ...

    @abstractmethod
    def get_subscription(self, external_id: str) -> Result[ProviderSubscriptionData, FatalError]:
        ...
