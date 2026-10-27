import json
from dataclasses import asdict, replace
from datetime import datetime, timezone
from typing import assert_never
from django.conf import settings
from django.db import transaction
from api.modules.logger import log
from api.src.domain.interface.payment.data import Money
from api.src.domain.interface.payment.provider.data import CancelResult, CancelSuccess, CheckoutData, CheckoutResult, CustomerData, MarketplaceData, ProviderSubscriptionData, RedirectUrls, WebhookVerifyResult
from api.src.domain.interface.payment.provider.interface import PaymentInterface
from api.src.domain.interface.payment.subscription.data import SubscriptionData
from api.src.domain.interface.payment.subscription.interface import FilterOption as SubscriptionFilterOption, SortOption as SubscriptionSortOption, SubscriptionInterface
from api.src.domain.interface.payment.transaction.interface import FilterOption as TransactionFilterOption, SortOption as TransactionSortOption, TransactionInterface
from api.src.domain.interface.user.data import UserAllData
from api.src.domain.interface.webhook.inbox.data import WebhookInboxData
from api.src.domain.interface.webhook.inbox.interface import FilterOption as WebhookInboxFilterOption, SortOption as WebhookInboxSortOption, WebhookInboxInterface
from api.src.domain.interface.webhook.outbox.data import WebhookOutboxData
from api.src.domain.interface.webhook.outbox.interface import WebhookOutboxInterface
from api.src.injectors.container import injector
from api.src.types.dto.webhook import WebhookOutboxPayloadDTO
from api.src.usecase.user import get_user_data, save_user_data
from api.utils.common.result import FatalError, FindError, NotFoundError, Result
from api.utils.enum.i18n import Currency, Locale
from api.utils.enum.payment import PaymentProvider, PaymentStatus, PaymentType, SubscriptionStatus, WebhookEventType, WebhookDeliveryStatus
from api.utils.enum.user import PlanName
from api.utils.functions.map import locale_path, payment_status_rank
from api.utils.plan import get_plan


@Result.shield_exception()
def create_checkout(user_id: int, plan_name: str, locale: Locale) -> Result[CheckoutResult, FindError]:
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

    frontend_url = f"{settings.FRONTEND_URL}{locale_path(locale)}"
    data = CheckoutData(
        product_code=plan.name,
        description=plan.description,
        price=Money(amount=plan.price, currency=Currency.JPY),
        payment_type=PaymentType.SUBSCRIPTION,
        customer=CustomerData(user_ulid=user.user.ulid, email=user.user.email),
        redirect=RedirectUrls(
            success_url=f"{frontend_url}/setting/payment/success",
            cancel_url=f"{frontend_url}/setting/payment/cancel",
        ),
        marketplace=MarketplaceData(seller_id="", application_fee=Money(amount=0, currency=Currency.JPY)),
        locale=locale,
    )

    repo = injector.get(PaymentInterface)
    checkout_ret = repo.create_checkout(data)
    if checkout_ret.is_err:
        return Result.err(checkout_ret.err_value)

    checkout = checkout_ret.ok_value
    return Result.ok(checkout)


@Result.shield_exception()
def verify_webhook(payload: bytes, signature: str) -> Result[WebhookVerifyResult, FatalError]:
    repo = injector.get(PaymentInterface)
    ret = repo.verify_webhook(payload, signature)
    if ret.is_err:
        return Result.err(ret.err_value)

    verification = ret.ok_value
    return Result.ok(verification)


@Result.shield_exception()
def cancel_subscription(user_id: int) -> Result[CancelResult, FindError]:
    repo = injector.get(SubscriptionInterface)
    ids_ret = repo.get_ids(SubscriptionFilterOption(customer_user_id=user_id, provider=PaymentProvider.STRIPE.value), SubscriptionSortOption(is_asc=False))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    subscriptions_ret = repo.bulk_get(ids)
    if subscriptions_ret.is_err:
        return Result.err(subscriptions_ret.err_value)

    subscriptions = subscriptions_ret.ok_value
    not_canceled_at = datetime.min.replace(tzinfo=timezone.utc)
    cancelable_subscriptions = [s for s in subscriptions if s.status in (SubscriptionStatus.ACTIVE, SubscriptionStatus.PAST_DUE) and s.canceled_at == not_canceled_at]
    if len(cancelable_subscriptions) == 0:
        return Result.err(NotFoundError("error.subscriptionNotFound"))

    subscription = cancelable_subscriptions[0]

    payment_repo = injector.get(PaymentInterface)
    cancel_ret = payment_repo.cancel_subscription(subscription.external_id)
    if cancel_ret.is_err:
        return Result.err(cancel_ret.err_value)

    cancellation = cancel_ret.ok_value
    if isinstance(cancellation, CancelSuccess):
        updated = replace(subscription, canceled_at=cancellation.canceled_at, current_period_end=cancellation.period_end)
        save_ret = repo.bulk_save([updated])
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
    repo = injector.get(WebhookInboxInterface)
    ids_ret = repo.get_ids(WebhookInboxFilterOption(provider=event.provider.value, event_id=event.event_id), WebhookInboxSortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) > 0:
        log.info("WebhookInbox already processed", event_id=event.event_id)
        return Result.ok(False)

    save_ret = repo.bulk_save([event])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(True)


@Result.shield_exception()
def dispatch_webhook_inbox(event: WebhookInboxData) -> Result[None, FatalError]:
    match event.event_type:
        case WebhookEventType.SUBSCRIPTION_CREATED | WebhookEventType.SUBSCRIPTION_UPDATED | WebhookEventType.SUBSCRIPTION_CANCELED:
            ret = update_subscription(event)
        case WebhookEventType.PAYMENT_SUCCEEDED:
            ret = update_transaction_status(event, PaymentStatus.CAPTURED, update_paid_at=True)
        case WebhookEventType.PAYMENT_FAILED:
            ret = update_transaction_status(event, PaymentStatus.FAILED, update_paid_at=False)
        case WebhookEventType.REFUND_ISSUED:
            ret = update_transaction_status(event, PaymentStatus.REFUNDED, update_paid_at=False)

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
def update_subscription(event: WebhookInboxData) -> Result[None, FatalError]:
    payment_repo = injector.get(PaymentInterface)
    provider_ret = payment_repo.get_subscription(event.external_id)
    if provider_ret.is_err:
        return Result.err(provider_ret.err_value)

    provider_subscription = provider_ret.ok_value
    if get_plan(provider_subscription.product_code) is None:
        log.error("Subscription unknown plan", external_id=event.external_id, product_code=provider_subscription.product_code)
        return Result.ok(None)

    if len(provider_subscription.user_ulid) == 0:
        log.error("Subscription user_ulid missing", external_id=event.external_id)
        return Result.ok(None)

    user_ret = get_user_data(ulid=provider_subscription.user_ulid)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        log.error("Subscription user not found", external_id=event.external_id, user_ulid=provider_subscription.user_ulid)
        return Result.ok(None)

    repo = injector.get(SubscriptionInterface)
    ids_ret = repo.get_ids(
        SubscriptionFilterOption(provider=provider_subscription.provider.value, external_id=provider_subscription.external_id),
        SubscriptionSortOption(),
        limit=1,
    )
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    subscription = SubscriptionData(
        id=ids[0] if len(ids) > 0 else 0,
        customer_user_id=user.user.id,
        seller_id="",
        provider=provider_subscription.provider,
        external_id=provider_subscription.external_id,
        product_code=provider_subscription.product_code,
        price=provider_subscription.price,
        status=provider_subscription.status,
        started_at=provider_subscription.started_at,
        current_period_end=provider_subscription.current_period_end,
        canceled_at=provider_subscription.canceled_at,
    )
    subscription_ret = save_subscription_data(subscription)
    if subscription_ret.is_err:
        return Result.err(subscription_ret.err_value)

    user_plan_ret = update_user_plan(user, provider_subscription)
    if user_plan_ret.is_err:
        return Result.err(user_plan_ret.err_value)

    log.info("Subscription updated", external_id=event.external_id, status=provider_subscription.status.value)
    return Result.ok(None)


@Result.shield_exception()
def save_subscription_data(data: SubscriptionData) -> Result[None, FatalError]:
    repo = injector.get(SubscriptionInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def update_user_plan(user: UserAllData, provider_subscription: ProviderSubscriptionData) -> Result[None, FatalError]:
    match provider_subscription.status:
        case SubscriptionStatus.ACTIVE | SubscriptionStatus.PAST_DUE:
            user_plan = replace(
                user.user_plan,
                plan=provider_subscription.product_code,
                customer_id=provider_subscription.customer_id,
                subscription=provider_subscription.external_id,
                is_paid=True,
                start_date=provider_subscription.started_at,
                end_date=provider_subscription.current_period_end,
            )
        case SubscriptionStatus.CANCELED | SubscriptionStatus.EXPIRED:
            if user.user_plan.subscription != provider_subscription.external_id:
                return Result.ok(None)

            user_plan = replace(user.user_plan, plan=PlanName.FREE, is_paid=False, end_date=provider_subscription.current_period_end)
        case SubscriptionStatus.INCOMPLETE:
            return Result.ok(None)
        case _:
            assert_never(provider_subscription.status)

    ret = save_user_data(replace(user, user_plan=user_plan))
    if ret.is_err:
        return Result.err(ret.err_value)

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
    if payment_status_rank(status) < payment_status_rank(payment_transaction.status):
        log.info("Transaction status not downgraded", external_id=event.external_id, current=payment_transaction.status.value, status=status.value)
        return Result.ok(None)

    updated = replace(payment_transaction, status=status, paid_at=event.occurred_at) if update_paid_at else replace(payment_transaction, status=status)
    save_ret = repo.bulk_save([updated])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    log.info("Transaction status updated", external_id=event.external_id, status=status.value)
    return Result.ok(None)
