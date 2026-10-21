from collections.abc import Callable
from datetime import date
import pytest
from api.db.models.user import MyPage, Profile, User, UserNotification, UserPlan
from api.src.domain.interface.payment.provider.interface import PaymentInterface
from api.src.injectors.container import injector
from api.tests.fakes import FakePayment


PASSWORD = "password1234"


@pytest.fixture
def make_user(db: None) -> Callable[[str], User]:
    def make(name: str) -> User:
        user = User.objects.create_user(email=f"{name}@example.com", username=name, nickname=name, password=PASSWORD)
        user.is_active = True
        user.save()
        Profile.objects.create(user=user, last_name="last", first_name="first", birthday=date(2000, 1, 1))
        MyPage.objects.create(user=user, content="")
        UserNotification.objects.create(user=user)
        UserPlan.objects.create(user=user, customer_id="", subscription="")
        saved_user: User = User.objects.get(id=user.id)
        return saved_user

    return make


@pytest.fixture
def fake_payment(monkeypatch: pytest.MonkeyPatch) -> FakePayment:
    fake = FakePayment()
    binding = injector.binder.create_binding(PaymentInterface, to=fake)
    monkeypatch.setitem(injector.binder._bindings, PaymentInterface, binding)
    return fake
