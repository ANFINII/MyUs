import hashlib
import hmac
import json
import time
from typing import Any
import pytest
from api.src.adapter.external.payment.stripe.provider import StripeProvider
from api.src.domain.interface.payment.event.data import ProviderSubscriptionData
from api.src.domain.interface.payment.provider.data import WebhookVerified, WebhookVerifyFailed
from api.utils.enum.payment import SubscriptionStatus, WebhookEventType, WebhookVerifyError


SECRET = "whsec_test"


def signature(payload: bytes, secret: str) -> str:
    timestamp = int(time.time())
    signed = f"{timestamp}.{payload.decode()}".encode()
    digest = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


def event_payload(event_type: str) -> bytes:
    event = {
        "id": "evt_1",
        "object": "event",
        "type": event_type,
        "created": 1700000000,
        "data": {"object": {
            "id": "sub_1",
            "object": "subscription",
            "customer": "cus_1",
            "metadata": {"user_ulid": "01USER", "product_code": "Premium"},
            "items": {"object": "list", "data": [{"object": "subscription_item", "current_period_end": 1702592000, "price": {"object": "price", "unit_amount": 1200, "currency": "jpy"}}]},
            "status": "active",
            "start_date": 1700000000,
            "canceled_at": None,
        }},
    }
    return json.dumps(event).encode()


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
