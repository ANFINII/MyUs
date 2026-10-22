from collections.abc import Callable
from datetime import datetime, timezone
import pytest
from api.db.models.payment import Subscription
from api.db.models.user import User
from api.src.domain.interface.payment.provider.data import CancelFailed
from api.src.types.schema.auth import WithdrawalIn
from api.src.usecase.auth import withdraw_user
from api.src.usecase.payment import cancel_subscription
from api.tests.conftest import PASSWORD
from api.tests.fakes import FakePayment
from api.utils.enum.payment import CancelError, PaymentProvider, SubscriptionStatus
from api.utils.enum.user import PlanName


def add_subscription(user: User, external_id: str, status: SubscriptionStatus, month: int) -> None:
    Subscription.objects.create(
        customer=user,
        provider=PaymentProvider.STRIPE,
        external_id=external_id,
        product_code=PlanName.PREMIUM,
        status=status,
        started_at=datetime(2026, month, 1, tzinfo=timezone.utc),
    )


def withdraw(user: User, password: str = PASSWORD) -> str:
    ret = withdraw_user(user.id, WithdrawalIn(password=password))
    assert ret.is_ok, ret
    message = ret.ok_value
    return message


def is_active(user: User) -> bool:
    saved_user: User = User.objects.get(id=user.id)
    return saved_user.is_active


@pytest.mark.django_db
def test_free_user_withdraws_without_cancel(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")

    assert withdraw(user) == ""

    assert fake_payment.canceled_ids == []
    assert not is_active(user)


@pytest.mark.django_db
def test_active_subscription_is_canceled_before_withdraw(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    add_subscription(user, "sub_1", SubscriptionStatus.ACTIVE, 9)

    assert withdraw(user) == ""

    assert fake_payment.canceled_ids == ["sub_1"]
    assert not is_active(user)
    assert Subscription.objects.get(external_id="sub_1").current_period_end == datetime(2026, 11, 1, tzinfo=timezone.utc)


@pytest.mark.django_db
def test_cancel_failure_keeps_user_active(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    add_subscription(user, "sub_1", SubscriptionStatus.ACTIVE, 9)
    fake_payment.cancel_result = CancelFailed(error=CancelError.NETWORK_ERROR, message="timeout")

    assert withdraw(user) == "error.cancelFailed"

    assert is_active(user)


@pytest.mark.django_db
def test_subscription_missing_on_stripe_still_withdraws(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    add_subscription(user, "sub_1", SubscriptionStatus.ACTIVE, 9)
    fake_payment.cancel_result = CancelFailed(error=CancelError.NOT_FOUND, message="no such subscription")

    assert withdraw(user) == ""

    assert not is_active(user)


@pytest.mark.django_db
def test_wrong_password_does_not_cancel(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    add_subscription(user, "sub_1", SubscriptionStatus.ACTIVE, 9)

    assert withdraw(user, "wrong-password") == "error.passwordWrong"

    assert fake_payment.canceled_ids == []
    assert is_active(user)


@pytest.mark.django_db
def test_latest_cancelable_subscription_is_canceled(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    add_subscription(user, "sub_old", SubscriptionStatus.ACTIVE, 8)
    add_subscription(user, "sub_new", SubscriptionStatus.CANCELED, 10)
    add_subscription(user, "sub_due", SubscriptionStatus.PAST_DUE, 9)

    assert withdraw(user) == ""

    assert fake_payment.canceled_ids == ["sub_due"]


@pytest.mark.django_db
def test_scheduled_cancel_is_not_canceled_again(make_user: Callable[[str], User], fake_payment: FakePayment) -> None:
    user = make_user("alice")
    add_subscription(user, "sub_1", SubscriptionStatus.ACTIVE, 9)

    first_ret = cancel_subscription(user.id)
    second_ret = cancel_subscription(user.id)

    assert first_ret.is_ok
    assert second_ret.is_err
    assert fake_payment.canceled_ids == ["sub_1"]

    assert withdraw(user) == ""

    assert fake_payment.canceled_ids == ["sub_1"]
    assert not is_active(user)
