from datetime import datetime, timezone
from io import StringIO
import pytest
from django.core.management import call_command
from api.db.models.payment import WebhookOutbox
from api.utils.enum.payment import PaymentProvider, WebhookDeliveryStatus, WebhookEventType


def add_outbox(external_id: str, status: WebhookDeliveryStatus) -> None:
    WebhookOutbox.objects.create(
        provider=PaymentProvider.STRIPE,
        event_type=WebhookEventType.SUBSCRIPTION_CREATED,
        external_id=external_id,
        payload="{}",
        status=status,
        occurred_at=datetime(2026, 10, 1, tzinfo=timezone.utc),
    )


def dispatch() -> str:
    out = StringIO()
    call_command("dispatch_webhook_outbox", stdout=out)
    return out.getvalue()


@pytest.mark.django_db
def test_pending_entries_are_delivered() -> None:
    add_outbox("sub_1", WebhookDeliveryStatus.PENDING)
    add_outbox("sub_2", WebhookDeliveryStatus.PENDING)
    add_outbox("sub_3", WebhookDeliveryStatus.DELIVERED)

    assert "Dispatched 2 webhook outbox entries" in dispatch()

    assert WebhookOutbox.objects.filter(status=WebhookDeliveryStatus.PENDING).count() == 0
    delivered = WebhookOutbox.objects.get(external_id="sub_1")
    assert delivered.status == WebhookDeliveryStatus.DELIVERED
    assert delivered.delivered_at.year == datetime.now(timezone.utc).year


@pytest.mark.django_db
def test_no_pending_entries() -> None:
    add_outbox("sub_1", WebhookDeliveryStatus.DELIVERED)

    assert "No pending webhook outbox entries" in dispatch()
