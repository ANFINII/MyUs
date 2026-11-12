from abc import ABC, abstractmethod
from myus.domain.interface.payment.event.data import ProviderSubscriptionData
from myus.domain.interface.payment.provider.data import CancelResult, CheckoutData, CheckoutResult, PaymentMethodSessionResult, PlanChangeResult, RevokeResult, WebhookVerifyResult
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.i18n import Locale


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

    @abstractmethod
    def create_payment_method_session(self, customer_id: str, return_url: str, locale: Locale) -> Result[PaymentMethodSessionResult, FatalError]:
        ...
