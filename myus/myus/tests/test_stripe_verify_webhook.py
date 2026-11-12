import hashlib
import hmac
import json
import time
from typing import Any
import pytest
import stripe
from myus.adapter.external.payment.stripe.provider import StripeProvider
from myus.domain.interface.payment.event.data import ProviderSubscriptionData
from myus.domain.interface.payment.provider.data import WebhookVerified, WebhookVerifyFailed
from myus.utils.enum.payment import SubscriptionStatus, WebhookEventType, WebhookVerifyError


SECRET = "whsec_test"


def signature(payload: bytes, secret: str) -> str:
    timestamp = int(time.time())
    signed = f"{timestamp}.{payload.decode()}".encode()
    digest = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


SUBSCRIPTION_OBJECT: dict[str, Any] = {
    "id": "sub_1",
    "object": "subscription",
    "customer": "cus_1",
    "metadata": {"user_ulid": "01USER", "product_code": "Premium"},
    "items": {"object": "list", "data": [{"object": "subscription_item", "current_period_end": 1702592000, "price": {"object": "price", "unit_amount": 1200, "currency": "jpy"}}]},
    "status": "active",
    "start_date": 1700000000,
    "canceled_at": None,
}


def event_payload(event_type: str, obj: dict[str, Any] = SUBSCRIPTION_OBJECT) -> bytes:
    event = {
        "id": "evt_1",
        "object": "event",
        "type": event_type,
        "created": 1700000000,
        "data": {"object": obj},
    }
    return json.dumps(event).encode()


def assert_no_payment(payload: bytes) -> None:
    ret = StripeProvider().verify_webhook(payload, signature(payload, SECRET))

    assert ret.is_ok, ret
    verification = ret.ok_value
    assert isinstance(verification, WebhookVerifyFailed)
    assert verification.error == WebhookVerifyError.UNSUPPORTED_EVENT


@pytest.fixture(autouse=True)
def webhook_secret(settings: Any) -> None:
    settings.STRIPE_WEBHOOK_SECRET = SECRET


def test_valid_signature_is_verified() -> None:
    payload = event_payload("customer.subscription.created")

    ret = StripeProvider().verify_webhook(payload, signature(payload, SECRET))

    assert ret.is_ok, ret
    verification = ret.ok_value
    assert isinstance(verification, WebhookVerified)
    assert verification.event.event_id == "evt_1"
    assert verification.event.event_type == WebhookEventType.SUBSCRIPTION_CREATED
    assert verification.event.external_id == "sub_1"
    assert verification.event.payload == payload.decode()
    content = verification.event.content
    assert isinstance(content, ProviderSubscriptionData)
    assert content.customer_id == "cus_1"
    assert content.user_ulid == "01USER"
    assert content.status == SubscriptionStatus.ACTIVE


def test_wrong_secret_is_rejected() -> None:
    payload = event_payload("customer.subscription.created")

    ret = StripeProvider().verify_webhook(payload, signature(payload, "whsec_other"))

    assert ret.is_ok, ret
    verification = ret.ok_value
    assert isinstance(verification, WebhookVerifyFailed)
    assert verification.error == WebhookVerifyError.INVALID_SIGNATURE


def test_unsupported_event_is_reported() -> None:
    payload = event_payload("invoice.created")

    ret = StripeProvider().verify_webhook(payload, signature(payload, SECRET))

    assert ret.is_ok, ret
    verification = ret.ok_value
    assert isinstance(verification, WebhookVerifyFailed)
    assert verification.error == WebhookVerifyError.UNSUPPORTED_EVENT


def test_malformed_payload_is_reported() -> None:
    payload = b"not json"

    ret = StripeProvider().verify_webhook(payload, signature(payload, SECRET))

    assert ret.is_ok, ret
    verification = ret.ok_value
    assert isinstance(verification, WebhookVerifyFailed)
    assert verification.error == WebhookVerifyError.MALFORMED_PAYLOAD


def test_zero_yen_invoice_paid_is_not_recorded() -> None:
    assert_no_payment(event_payload("invoice.paid", {"id": "in_1", "object": "invoice", "amount_paid": 0}))


def test_invoice_failed_without_payment_intent_is_not_recorded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(stripe.InvoicePayment, "list", lambda **params: stripe.ListObject.construct_from({"object": "list", "data": []}, None))

    assert_no_payment(event_payload("invoice.payment_failed", {"id": "in_1", "object": "invoice", "amount_paid": 0}))


def test_invoice_failed_uses_open_payment(monkeypatch: pytest.MonkeyPatch) -> None:
    payments = [
        {"object": "invoice_payment", "status": "canceled", "payment": {"type": "payment_intent", "payment_intent": "pi_canceled"}},
        {"object": "invoice_payment", "status": "open", "payment": {"type": "payment_intent", "payment_intent": "pi_open"}},
    ]
    monkeypatch.setattr(stripe.InvoicePayment, "list", lambda **params: stripe.ListObject.construct_from({"object": "list", "data": [p for p in payments if p["status"] == params["status"]]}, None))
    payload = event_payload("invoice.payment_failed", {"id": "in_1", "object": "invoice", "amount_paid": 0})

    ret = StripeProvider().verify_webhook(payload, signature(payload, SECRET))

    assert ret.is_ok, ret
    verification = ret.ok_value
    assert isinstance(verification, WebhookVerified)
    assert verification.event.external_id == "pi_open"


def test_refund_without_payment_intent_is_not_recorded() -> None:
    assert_no_payment(event_payload("charge.refunded", {"id": "ch_1", "object": "charge", "payment_intent": None}))
