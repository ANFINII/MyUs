import json
from dataclasses import asdict, replace
from datetime import datetime, timezone
from django.conf import settings
from django.db import transaction
from api.modules.logger import log
from api.src.domain.interface.payment.data import Money
from api.src.domain.interface.payment.provider.data import CancelResult, CancelSuccess, CheckoutData, CheckoutResult, CustomerData, MarketplaceData, RedirectUrls, WebhookVerifyResult
from api.src.domain.interface.payment.provider.interface import PaymentInterface
from api.src.domain.interface.payment.subscription.interface import FilterOption as SubscriptionFilterOption, SortOption as SubscriptionSortOption, SubscriptionInterface
from api.src.domain.interface.payment.transaction.interface import FilterOption as TransactionFilterOption, SortOption as TransactionSortOption, TransactionInterface
from api.src.domain.interface.webhook.inbox.data import WebhookInboxData
from api.src.domain.interface.webhook.inbox.interface import FilterOption as WebhookInboxFilterOption, SortOption as WebhookInboxSortOption, WebhookInboxInterface
from api.src.domain.interface.webhook.outbox.data import WebhookOutboxData
from api.src.domain.interface.webhook.outbox.interface import WebhookOutboxInterface
from api.src.injectors.container import injector
from api.src.types.dto.webhook import WebhookOutboxPayloadDTO
from api.src.usecase.user import get_user_data
from api.utils.common.result import FatalError, NotFoundError, Result
from api.utils.enum.i18n import Currency, Locale
from api.utils.enum.payment import PaymentProvider, PaymentStatus, PaymentType, SubscriptionStatus, WebhookEventType, WebhookDeliveryStatus
from api.utils.plan import get_plan


@Result.shield_exception()
def create_checkout(user_id: int, plan_name: str) -> Result[CheckoutResult, NotFoundError | FatalError]:
    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        return Result.err(NotFoundError("Not Found"))

    plan = get_plan(plan_name)
    if plan is None:
        log.warning("Payment unknown plan", plan=plan_name)
        return Result.err(NotFoundError("Not Found"))

    data = CheckoutData(
        product_code=plan.name,
        description=plan.description,
        price=Money(amount=plan.price, currency=Currency.JPY),
        payment_type=PaymentType.SUBSCRIPTION,
        customer=CustomerData(email=user.user.email),
        redirect=RedirectUrls(
            success_url=f"{settings.FRONTEND_URL}/setting/payment/success",
            cancel_url=f"{settings.FRONTEND_URL}/setting/payment/cancel",
        ),
        marketplace=MarketplaceData(seller_id="", application_fee=Money(amount=0, currency=Currency.JPY)),
        locale=Locale.JA,
    )

    payment = injector.get(PaymentInterface)
    checkout_ret = payment.create_checkout(data)
    if checkout_ret.is_err:
        return Result.err(checkout_ret.err_value)

    checkout = checkout_ret.ok_value
    return Result.ok(checkout)


@Result.shield_exception()
def verify_webhook(payload: bytes, signature: str) -> Result[WebhookVerifyResult, FatalError]:
    payment = injector.get(PaymentInterface)
    ret = payment.verify_webhook(payload, signature)
    if ret.is_err:
        return Result.err(ret.err_value)

    verification = ret.ok_value
    return Result.ok(verification)


@Result.shield_exception()
def cancel_subscription(user_id: int) -> Result[CancelResult, NotFoundError | FatalError]:
    repository = injector.get(SubscriptionInterface)
    ids_ret = repository.get_ids(SubscriptionFilterOption(customer_user_id=user_id, provider=PaymentProvider.STRIPE.value), SubscriptionSortOption(is_asc=False), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.err(NotFoundError("アクティブなサブスクリプションが見つかりません"))

    subscriptions_ret = repository.bulk_get(ids)
    if subscriptions_ret.is_err:
        return Result.err(subscriptions_ret.err_value)

    subscriptions = subscriptions_ret.ok_value
    subscription = subscriptions[0]
    if subscription.status != SubscriptionStatus.ACTIVE:
        return Result.err(NotFoundError("アクティブなサブスクリプションが見つかりません"))

    payment = injector.get(PaymentInterface)
    cancel_ret = payment.cancel_subscription(subscription.external_id)
    if cancel_ret.is_err:
        return Result.err(cancel_ret.err_value)

    cancellation = cancel_ret.ok_value
    if isinstance(cancellation, CancelSuccess):
        updated = replace(subscription, canceled_at=cancellation.canceled_at, current_period_end=cancellation.period_end)
        save_ret = repository.bulk_save([updated])
        if save_ret.is_err:
            return Result.err(save_ret.err_value)

        log.info("Payment cancel succeeded", user_id=user_id, external_id=subscription.external_id)

    return Result.ok(cancellation)


@Result.shield_exception()
def receive_webhook_inbox(event: WebhookInboxData) -> Result[bool, FatalError]:
    with transaction.atomic():
        enqueue_inbox_ret = enqueue_webhook_inbox(event)
        if enqueue_inbox_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(enqueue_inbox_ret.err_value)

        is_enqueued = enqueue_inbox_ret.ok_value
        if not is_enqueued:
            return Result.ok(False)

        dispatch_ret = dispatch_webhook_inbox(event)
        if dispatch_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(dispatch_ret.err_value)

        enqueue_outbox_ret = enqueue_webhook_outbox(event)
        if enqueue_outbox_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(enqueue_outbox_ret.err_value)

    return Result.ok(True)


@Result.shield_exception()
def enqueue_webhook_inbox(event: WebhookInboxData) -> Result[bool, FatalError]:
    repository = injector.get(WebhookInboxInterface)
    ids_ret = repository.get_ids(WebhookInboxFilterOption(provider=event.provider.value, event_id=event.event_id), WebhookInboxSortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) > 0:
        log.info("WebhookInbox already processed", event_id=event.event_id)
        return Result.ok(False)

    save_ret = repository.bulk_save([event])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(True)


@Result.shield_exception()
def dispatch_webhook_inbox(event: WebhookInboxData) -> Result[None, FatalError]:
    match event.event_type:
        case WebhookEventType.SUBSCRIPTION_CANCELED:
            ret = update_subscription_canceled(event)
        case WebhookEventType.PAYMENT_SUCCEEDED:
            ret = update_transaction_status(event, PaymentStatus.CAPTURED, update_paid_at=True)
        case WebhookEventType.PAYMENT_FAILED:
            ret = update_transaction_status(event, PaymentStatus.FAILED, update_paid_at=False)
        case WebhookEventType.REFUND_ISSUED:
            ret = update_transaction_status(event, PaymentStatus.REFUNDED, update_paid_at=False)
        case WebhookEventType.SUBSCRIPTION_CREATED:
            log.info("WebhookInbox SUBSCRIPTION_CREATED noop", external_id=event.external_id)
            return Result.ok(None)
        case WebhookEventType.SUBSCRIPTION_UPDATED:
            log.info("WebhookInbox SUBSCRIPTION_UPDATED noop", external_id=event.external_id)
            return Result.ok(None)

    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def enqueue_webhook_outbox(event: WebhookInboxData) -> Result[None, FatalError]:
    repo = injector.get(WebhookOutboxInterface)

    payload = WebhookOutboxPayloadDTO(
        provider=event.provider.value,
        event_id=event.event_id,
        event_type=event.event_type.value,
        external_id=event.external_id,
        occurred_at=event.occurred_at.isoformat(),
    )

    data = WebhookOutboxData(
        id=0,
        provider=event.provider,
        event_type=event.event_type,
        external_id=event.external_id,
        payload=json.dumps(asdict(payload)),
        status=WebhookDeliveryStatus.PENDING,
        occurred_at=event.occurred_at,
        delivered_at=datetime.min.replace(tzinfo=timezone.utc),
    )

    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    log.info("WebhookOutbox enqueued", event_id=event.event_id, event_type=event.event_type.value)
    return Result.ok(None)


@Result.shield_exception()
def update_subscription_canceled(event: WebhookInboxData) -> Result[None, FatalError]:
    repo = injector.get(SubscriptionInterface)
    ids_ret = repo.get_ids(
        SubscriptionFilterOption(provider=event.provider.value, external_id=event.external_id),
        SubscriptionSortOption(),
        limit=1,
    )
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("Subscription not found for cancel", external_id=event.external_id)
        return Result.ok(None)

    subs_ret = repo.bulk_get(ids)
    if subs_ret.is_err:
        return Result.err(subs_ret.err_value)

    subs = subs_ret.ok_value
    updated = replace(subs[0], status=SubscriptionStatus.CANCELED, canceled_at=event.occurred_at)
    save_ret = repo.bulk_save([updated])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    log.info("Subscription canceled", external_id=event.external_id)
    return Result.ok(None)


@Result.shield_exception()
def update_transaction_status(event: WebhookInboxData, status: PaymentStatus, update_paid_at: bool) -> Result[None, FatalError]:
    repo = injector.get(TransactionInterface)
    ids_ret = repo.get_ids(
        TransactionFilterOption(provider=event.provider.value, external_id=event.external_id),
        TransactionSortOption(),
        limit=1,
    )
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("Transaction not found for status update", external_id=event.external_id, status=status.value)
        return Result.ok(None)

    transactions_ret = repo.bulk_get(ids)
    if transactions_ret.is_err:
        return Result.err(transactions_ret.err_value)

    transactions = transactions_ret.ok_value
    payment_transaction = transactions[0]
    updated = replace(payment_transaction, status=status, paid_at=event.occurred_at) if update_paid_at else replace(payment_transaction, status=status)
    save_ret = repo.bulk_save([updated])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    log.info("Transaction status updated", external_id=event.external_id, status=status.value)
    return Result.ok(None)
