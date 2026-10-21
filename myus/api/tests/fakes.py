from datetime import datetime, timezone
from api.src.domain.interface.payment.data import Money
from api.src.domain.interface.payment.provider.data import CancelResult, CancelSuccess, CheckoutData, CheckoutResult, ProviderSubscriptionData, WebhookVerifyResult
from api.src.domain.interface.payment.provider.interface import PaymentInterface
from api.utils.common.result import FatalError, Result
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import PaymentProvider, SubscriptionStatus


class FakePayment(PaymentInterface):
    def __init__(self) -> None:
        self.subscriptions: dict[str, ProviderSubscriptionData] = {}
        self.canceled_ids: list[str] = []
        self.cancel_result: CancelResult = CancelSuccess(
            canceled_at=datetime(2026, 10, 15, tzinfo=timezone.utc),
            period_end=datetime(2026, 11, 1, tzinfo=timezone.utc),
        )

    def create_checkout(self, input: CheckoutData) -> Result[CheckoutResult, FatalError]:
        raise NotImplementedError

    def verify_webhook(self, payload: bytes, signature: str) -> Result[WebhookVerifyResult, FatalError]:
        raise NotImplementedError

    def cancel_subscription(self, external_id: str) -> Result[CancelResult, FatalError]:
        self.canceled_ids.append(external_id)
        return Result.ok(self.cancel_result)

    def get_subscription(self, external_id: str) -> Result[ProviderSubscriptionData, FatalError]:
        return Result.ok(self.subscriptions[external_id])


def provider_subscription(external_id: str, user_ulid: str, product_code: str, status: SubscriptionStatus) -> ProviderSubscriptionData:
    return ProviderSubscriptionData(
        provider=PaymentProvider.STRIPE,
        external_id=external_id,
        customer_id="cus_test",
        user_ulid=user_ulid,
        product_code=product_code,
        price=Money(amount=1200, currency=Currency.JPY),
        status=status,
        started_at=datetime(2026, 10, 1, tzinfo=timezone.utc),
        current_period_end=datetime(2026, 11, 1, tzinfo=timezone.utc),
        canceled_at=datetime.min.replace(tzinfo=timezone.utc),
    )
