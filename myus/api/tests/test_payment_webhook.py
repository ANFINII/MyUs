import threading
from collections.abc import Callable
from datetime import datetime, timezone
import pytest
from django.db import connection
from api.db.models.payment import PaymentEvent, PaymentLedgerEntry, PaymentPayout, PaymentTransaction, Subscription, WebhookOutbox
from api.db.models.user import User, UserPlan
from api.src.domain.interface.payment.event.data import BalanceData, PaymentEventContent, PaymentEventData, PaymentFailedContent, PaymentPaidContent, PayoutContent, RefundContent
from api.src.usecase.payment import receive_payment_event
from api.tests.fakes import provider_subscription
from api.utils.common.result import FatalError, Result
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import LedgerEntryType, PaymentProvider, PaymentStatus, PayoutStatus, SubscriptionStatus, WebhookEventType
from api.utils.enum.user import PlanName


def receive(event_type: WebhookEventType, external_id: str, event_id: str, content: PaymentEventContent, occurred_at: datetime | None = None) -> Result[bool, FatalError]:
    return receive_payment_event(PaymentEventData(
        id=0,
        provider=PaymentProvider.STRIPE,
        event_id=event_id,
        event_type=event_type,
        external_id=external_id,
        payload="{}",
        content=content,
        occurred_at=occurred_at or datetime.now(timezone.utc),
    ))


def send(event_type: WebhookEventType, external_id: str, event_id: str, content: PaymentEventContent, occurred_at: datetime | None = None) -> bool:
    ret = receive(event_type, external_id, event_id, content, occurred_at)
    assert ret.is_ok, ret
    is_received = ret.ok_value
    return is_received


def send_subscription(event_type: WebhookEventType, user: User, external_id: str, status: SubscriptionStatus, event_id: str, plan: str = PlanName.PREMIUM, occurred_at: datetime | None = None) -> bool:
    return send(event_type, external_id, event_id, provider_subscription(external_id, user.ulid, plan, status), occurred_at)


def balance(external_id: str, amount: int, fee: int) -> BalanceData:
    return BalanceData(external_id=external_id, amount=amount, fee=fee, currency=Currency.JPY, occurred_at=datetime(2026, 10, 1, tzinfo=timezone.utc))


def paid(user: User, subscription_external_id: str = "sub_1") -> PaymentPaidContent:
    return PaymentPaidContent(
        customer_id="cus_test",
        user_ulid=user.ulid,
        subscription_external_id=subscription_external_id,
        receipt_number="INV-0001",
        balance=balance("txn_1", 1100, 40),
    )


def user_plan(user: User) -> UserPlan:
    return UserPlan.objects.get(user=user)


def transaction_status(external_id: str) -> str:
    transaction: PaymentTransaction = PaymentTransaction.objects.get(external_id=external_id)
    return transaction.status


def ledger(entry_type: LedgerEntryType) -> list[tuple[str, int, int]]:
    return list(PaymentLedgerEntry.objects.filter(entry_type=entry_type).order_by("id").values_list("external_id", "amount", "tax_amount"))


@pytest.mark.django_db
def test_subscription_created_sets_paid_plan(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")

    assert send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_1")

    plan = user_plan(user)
    assert plan.plan == PlanName.PREMIUM
    assert plan.is_paid
    subscription = Subscription.objects.get(external_id="sub_1")
    assert subscription.payment_customer.user_id == user.id
    assert subscription.payment_customer.external_id == "cus_test"
    assert subscription.status == SubscriptionStatus.ACTIVE


@pytest.mark.django_db
def test_cancel_keeps_plan_until_subscription_deleted(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")
    send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_1")

    send_subscription(WebhookEventType.SUBSCRIPTION_UPDATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_2")
    assert user_plan(user).plan == PlanName.PREMIUM

    send_subscription(WebhookEventType.SUBSCRIPTION_CANCELED, user, "sub_1", SubscriptionStatus.CANCELED, "evt_3")

    plan = user_plan(user)
    assert plan.plan == PlanName.FREE
    assert not plan.is_paid
    assert Subscription.objects.get(external_id="sub_1").status == SubscriptionStatus.CANCELED
    assert Subscription.objects.count() == 1


@pytest.mark.django_db
def test_old_subscription_end_does_not_downgrade_new_plan(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")
    send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_old", SubscriptionStatus.ACTIVE, "evt_1")
    send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_new", SubscriptionStatus.ACTIVE, "evt_2", plan=PlanName.BASIC)

    send_subscription(WebhookEventType.SUBSCRIPTION_CANCELED, user, "sub_old", SubscriptionStatus.CANCELED, "evt_3")

    assert user_plan(user).plan == PlanName.BASIC


@pytest.mark.django_db
def test_older_subscription_event_is_not_applied(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")
    send_subscription(WebhookEventType.SUBSCRIPTION_UPDATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_2", occurred_at=datetime(2026, 11, 2, tzinfo=timezone.utc))

    assert send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.INCOMPLETE, "evt_1", occurred_at=datetime(2026, 11, 1, tzinfo=timezone.utc))

    subscription = Subscription.objects.get(external_id="sub_1")
    assert subscription.status == SubscriptionStatus.ACTIVE
    assert subscription.last_event_at == datetime(2026, 11, 2, tzinfo=timezone.utc)
    assert PaymentEvent.objects.count() == 2


@pytest.mark.django_db
def test_incomplete_subscription_does_not_change_plan(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")

    send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.INCOMPLETE, "evt_1", plan=PlanName.ULTIMATE)

    assert user_plan(user).plan == PlanName.FREE
    assert Subscription.objects.get(external_id="sub_1").status == SubscriptionStatus.INCOMPLETE


@pytest.mark.django_db
def test_subscription_without_user_is_skipped(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")

    assert send(WebhookEventType.SUBSCRIPTION_CREATED, "sub_1", "evt_1", provider_subscription("sub_1", "", PlanName.PREMIUM, SubscriptionStatus.ACTIVE))

    assert user_plan(user).plan == PlanName.FREE
    assert not Subscription.objects.filter(external_id="sub_1").exists()


@pytest.mark.django_db
def test_same_event_is_processed_once(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")

    assert send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_dup")
    assert not send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_dup")

    assert PaymentEvent.objects.filter(event_id="evt_dup").count() == 1
    assert WebhookOutbox.objects.count() == 1


@pytest.mark.django_db(transaction=True)
def test_same_event_arriving_at_once_is_processed_once(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")
    results: list[bool] = []

    def run() -> None:
        try:
            results.append(send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_at_once"))
        finally:
            connection.close()

    threads = [threading.Thread(target=run) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert sorted(results) == [False, False, False, True]
    assert PaymentEvent.objects.filter(event_id="evt_at_once").count() == 1
    assert WebhookOutbox.objects.count() == 1


@pytest.mark.django_db
def test_payment_records_sale_and_fee(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")
    send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_1")

    assert send(WebhookEventType.PAYMENT_SUCCEEDED, "pi_1", "evt_2", paid(user))

    transaction = PaymentTransaction.objects.get(external_id="pi_1")
    assert transaction.status == PaymentStatus.CAPTURED
    assert transaction.subscription is not None
    assert transaction.subscription.external_id == "sub_1"
    assert transaction.receipt_number == "INV-0001"
    assert transaction.tax_rate == 10
    assert ledger(LedgerEntryType.SALE) == [("txn_1", 1100, 100)]
    assert ledger(LedgerEntryType.FEE) == [("txn_1", -40, 0)]


@pytest.mark.django_db
def test_payment_before_subscription_is_retried(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")

    ret = receive(WebhookEventType.PAYMENT_SUCCEEDED, "pi_1", "evt_2", paid(user))

    assert ret.is_err
    assert not PaymentEvent.objects.exists()
    assert not PaymentTransaction.objects.exists()

    send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_1")
    assert send(WebhookEventType.PAYMENT_SUCCEEDED, "pi_1", "evt_2", paid(user))
    assert ledger(LedgerEntryType.SALE) == [("txn_1", 1100, 100)]


@pytest.mark.django_db
def test_partial_refunds_are_recorded_once_each(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")
    send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_1")
    send(WebhookEventType.PAYMENT_SUCCEEDED, "pi_1", "evt_2", paid(user))

    assert send(WebhookEventType.REFUND_ISSUED, "pi_1", "evt_3", RefundContent(balances=[balance("txn_r1", -550, 0)]))
    assert send(WebhookEventType.REFUND_ISSUED, "pi_1", "evt_4", RefundContent(balances=[balance("txn_r1", -550, 0), balance("txn_r2", -330, 0)]))

    assert ledger(LedgerEntryType.REFUND) == [("txn_r1", -550, -50), ("txn_r2", -330, -30)]
    assert transaction_status("pi_1") == PaymentStatus.REFUNDED


@pytest.mark.django_db
def test_payout_links_ledger_entries(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")
    send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_1")
    send(WebhookEventType.PAYMENT_SUCCEEDED, "pi_1", "evt_2", paid(user))
    content = PayoutContent(amount=1060, currency=Currency.JPY, status=PayoutStatus.PAID, arrival_at=datetime(2026, 10, 8, tzinfo=timezone.utc), balance_external_ids=["txn_1"])

    assert send(WebhookEventType.PAYOUT_PAID, "po_1", "evt_3", content)

    payout = PaymentPayout.objects.get(external_id="po_1")
    assert payout.amount == 1060
    assert payout.status == PayoutStatus.PAID
    assert PaymentLedgerEntry.objects.filter(payout=payout).count() == 2
    assert PaymentLedgerEntry.objects.get(entry_type=LedgerEntryType.SALE).amount == 1100


@pytest.mark.django_db
def test_late_failed_does_not_overwrite_captured(make_user: Callable[[str], User]) -> None:
    user = make_user("alice")
    send_subscription(WebhookEventType.SUBSCRIPTION_CREATED, user, "sub_1", SubscriptionStatus.ACTIVE, "evt_1")

    assert send(WebhookEventType.PAYMENT_SUCCEEDED, "pi_1", "evt_2", paid(user))
    assert send(WebhookEventType.PAYMENT_FAILED, "pi_1", "evt_3", PaymentFailedContent())
    assert transaction_status("pi_1") == PaymentStatus.CAPTURED

    assert send(WebhookEventType.REFUND_ISSUED, "pi_1", "evt_4", RefundContent(balances=[balance("txn_r1", -1100, 0)]))
    assert send(WebhookEventType.PAYMENT_SUCCEEDED, "pi_1", "evt_5", paid(user))
    assert transaction_status("pi_1") == PaymentStatus.REFUNDED
    assert ledger(LedgerEntryType.SALE) == [("txn_1", 1100, 100)]
