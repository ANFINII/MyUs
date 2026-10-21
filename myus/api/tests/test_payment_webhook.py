from collections.abc import Callable
from datetime import datetime, timezone
import pytest
from api.db.models.payment import PaymentTransaction, Subscription, WebhookInbox, WebhookOutbox
from api.db.models.user import User, UserPlan
from api.src.domain.interface.webhook.inbox.data import WebhookInboxData
from api.src.usecase.payment import receive_webhook_inbox
from api.tests.fakes import FakePayment, provider_subscription
from api.utils.enum.payment import PaymentProvider, PaymentStatus, SubscriptionStatus, WebhookEventType
from api.utils.enum.user import PlanName


def send(event_type: WebhookEventType, external_id: str, event_id: str) -> bool:
    ret = receive_webhook_inbox(WebhookInboxData(
        id=0,
        provider=PaymentProvider.STRIPE,
        event_id=event_id,
        event_type=event_type,
        external_id=external_id,
        occurred_at=datetime.now(timezone.utc),
    ))
    assert ret.is_ok, ret
    is_received = ret.ok_value
    return is_received


def user_plan(user: User) -> UserPlan:
    return UserPlan.objects.get(user=user)


@pytest.mark.django_db
def test_subscription_created_sets_paid_plan(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    fake_payment.subscriptions["sub_1"] = provider_subscription("sub_1", user.ulid, PlanName.PREMIUM, SubscriptionStatus.ACTIVE)

    assert send(WebhookEventType.SUBSCRIPTION_CREATED, "sub_1", "evt_1")

    plan = user_plan(user)
    assert plan.plan == PlanName.PREMIUM
    assert plan.is_paid
    assert plan.subscription == "sub_1"
    assert plan.customer_id == "cus_test"
    subscription = Subscription.objects.get(external_id="sub_1")
    assert subscription.customer_id == user.id
    assert subscription.status == SubscriptionStatus.ACTIVE


@pytest.mark.django_db
def test_cancel_keeps_plan_until_subscription_deleted(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    fake_payment.subscriptions["sub_1"] = provider_subscription("sub_1", user.ulid, PlanName.PREMIUM, SubscriptionStatus.ACTIVE)
    send(WebhookEventType.SUBSCRIPTION_CREATED, "sub_1", "evt_1")

    send(WebhookEventType.SUBSCRIPTION_UPDATED, "sub_1", "evt_2")
    assert user_plan(user).plan == PlanName.PREMIUM

    fake_payment.subscriptions["sub_1"] = provider_subscription("sub_1", user.ulid, PlanName.PREMIUM, SubscriptionStatus.CANCELED)
    send(WebhookEventType.SUBSCRIPTION_CANCELED, "sub_1", "evt_3")

    plan = user_plan(user)
    assert plan.plan == PlanName.FREE
    assert not plan.is_paid
    assert Subscription.objects.get(external_id="sub_1").status == SubscriptionStatus.CANCELED
    assert Subscription.objects.count() == 1


@pytest.mark.django_db
def test_old_subscription_end_does_not_downgrade_new_plan(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    fake_payment.subscriptions["sub_old"] = provider_subscription("sub_old", user.ulid, PlanName.PREMIUM, SubscriptionStatus.ACTIVE)
    send(WebhookEventType.SUBSCRIPTION_CREATED, "sub_old", "evt_1")
    fake_payment.subscriptions["sub_new"] = provider_subscription("sub_new", user.ulid, PlanName.BASIC, SubscriptionStatus.ACTIVE)
    send(WebhookEventType.SUBSCRIPTION_CREATED, "sub_new", "evt_2")

    fake_payment.subscriptions["sub_old"] = provider_subscription("sub_old", user.ulid, PlanName.PREMIUM, SubscriptionStatus.CANCELED)
    send(WebhookEventType.SUBSCRIPTION_CANCELED, "sub_old", "evt_3")

    plan = user_plan(user)
    assert plan.plan == PlanName.BASIC
    assert plan.subscription == "sub_new"


@pytest.mark.django_db
def test_incomplete_subscription_does_not_change_plan(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    fake_payment.subscriptions["sub_1"] = provider_subscription("sub_1", user.ulid, PlanName.ULTIMATE, SubscriptionStatus.INCOMPLETE)

    send(WebhookEventType.SUBSCRIPTION_CREATED, "sub_1", "evt_1")

    assert user_plan(user).plan == PlanName.FREE
    assert Subscription.objects.get(external_id="sub_1").status == SubscriptionStatus.INCOMPLETE


@pytest.mark.django_db
def test_subscription_without_user_is_skipped(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    fake_payment.subscriptions["sub_1"] = provider_subscription("sub_1", "", PlanName.PREMIUM, SubscriptionStatus.ACTIVE)

    assert send(WebhookEventType.SUBSCRIPTION_CREATED, "sub_1", "evt_1")

    assert user_plan(user).plan == PlanName.FREE
    assert not Subscription.objects.filter(external_id="sub_1").exists()


@pytest.mark.django_db
def test_same_event_is_processed_once(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    fake_payment.subscriptions["sub_1"] = provider_subscription("sub_1", user.ulid, PlanName.PREMIUM, SubscriptionStatus.ACTIVE)

    assert send(WebhookEventType.SUBSCRIPTION_CREATED, "sub_1", "evt_dup")
    assert not send(WebhookEventType.SUBSCRIPTION_CREATED, "sub_1", "evt_dup")

    assert WebhookInbox.objects.filter(event_id="evt_dup").count() == 1
    assert WebhookOutbox.objects.count() == 1


def transaction_status(external_id: str) -> str:
    transaction: PaymentTransaction = PaymentTransaction.objects.get(external_id=external_id)
    return transaction.status


@pytest.mark.django_db
def test_late_failed_does_not_overwrite_captured(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    PaymentTransaction.objects.create(customer=user, provider=PaymentProvider.STRIPE, external_id="pi_1")

    assert send(WebhookEventType.PAYMENT_SUCCEEDED, "pi_1", "evt_1")
    assert send(WebhookEventType.PAYMENT_FAILED, "pi_1", "evt_2")
    assert transaction_status("pi_1") == PaymentStatus.CAPTURED

    assert send(WebhookEventType.REFUND_ISSUED, "pi_1", "evt_3")
    assert send(WebhookEventType.PAYMENT_SUCCEEDED, "pi_1", "evt_4")
    assert transaction_status("pi_1") == PaymentStatus.REFUNDED


@pytest.mark.django_db
def test_retry_succeeded_after_failed_is_captured(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    PaymentTransaction.objects.create(customer=user, provider=PaymentProvider.STRIPE, external_id="pi_1")

    assert send(WebhookEventType.PAYMENT_FAILED, "pi_1", "evt_1")
    assert transaction_status("pi_1") == PaymentStatus.FAILED

    assert send(WebhookEventType.PAYMENT_SUCCEEDED, "pi_1", "evt_2")
    assert transaction_status("pi_1") == PaymentStatus.CAPTURED
