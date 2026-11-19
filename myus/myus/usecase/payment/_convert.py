from dataclasses import replace
from datetime import datetime, timezone
from typing import assert_never
from myus.domain.es.interface import EventStoreInterface
from myus.domain.media.blog.interface import BlogInterface
from myus.domain.media.common import FilterOption as MediaFilterOption, PageOption as MediaPageOption, SortOption as MediaSortOption
from myus.domain.payment.customer.data import PaymentCustomerData
from myus.domain.payment.customer.interface import FilterOption as PaymentCustomerFilterOption, PageOption as PaymentCustomerPageOption, SortOption as PaymentCustomerSortOption, PaymentCustomerInterface
from myus.domain.payment.event.data import BalanceData, PaymentEventData, PaymentFailedContent, PaymentPaidContent, PayoutContent, ProviderSubscriptionData, PurchasePaidContent, RefundContent
from myus.domain.payment.event.interface import FilterOption as PaymentEventFilterOption, PageOption as PaymentEventPageOption, SortOption as PaymentEventSortOption, PaymentEventInterface
from myus.domain.payment.ledger.data import LedgerEntryData
from myus.domain.payment.ledger.interface import FilterOption as LedgerEntryFilterOption, PageOption as LedgerEntryPageOption, SortOption as LedgerEntrySortOption, LedgerEntryInterface
from myus.domain.payment.payout.data import PayoutData
from myus.domain.payment.payout.interface import FilterOption as PayoutFilterOption, PageOption as PayoutPageOption, SortOption as PayoutSortOption, PayoutInterface
from myus.domain.payment.plan import get_plan
from myus.domain.payment.provider.interface import PaymentInterface
from myus.domain.payment.purchase.data import PurchaseData
from myus.domain.payment.purchase.interface import FilterOption as PurchaseFilterOption, PageOption as PurchasePageOption, SortOption as PurchaseSortOption, PurchaseInterface
from myus.domain.payment.seller.data import PaymentSellerData
from myus.domain.payment.seller.interface import FilterOption as PaymentSellerFilterOption, PageOption as PaymentSellerPageOption, SortOption as PaymentSellerSortOption, PaymentSellerInterface
from myus.domain.payment.subscription.apply import replay
from myus.domain.payment.subscription.data import SubscriptionData
from myus.domain.payment.subscription.decide import accept_provider_state, request_cancellation, fail_cancellation
from myus.domain.payment.subscription.event import SUBSCRIPTION_AGGREGATE_TYPE, subscription_aggregate_id
from myus.domain.payment.subscription.interface import FilterOption as SubscriptionFilterOption, PageOption as SubscriptionPageOption, SortOption as SubscriptionSortOption, SubscriptionInterface
from myus.domain.payment.subscription.state import ActiveSubscription, EndedSubscription, IncompleteSubscription, PastDueSubscription, SubscriptionState, convert_status
from myus.domain.payment.transaction.data import TransactionData
from myus.domain.payment.transaction.interface import FilterOption as TransactionFilterOption, PageOption as TransactionPageOption, SortOption as TransactionSortOption, TransactionInterface
from myus.domain.user.data import UserAllData
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import AccessError, CommandError, FatalError, ForbiddenError, HistoryError, Result
from myus.utils.enum.i18n import Currency
from myus.utils.enum.payment import CancelError, LedgerEntryType, PaymentProvider, PaymentStatus, ProductType, SubscriptionStatus
from myus.utils.enum.user import PlanName
from myus.utils.functions.map import country_currency, payment_status_rank
from myus.utils.functions.payment import included_tax, parse_product_code
from ..es._convert import handle_command
from ..user._convert import save_user_data
from ..user.core import get_user_data


TAX_RATE = 10
PLATFORM_FEE_RATE = 15
REPLAY_BATCH_SIZE = 100
PAYMENT_EVENT_MAX_ATTEMPTS = 30


def get_payment_repository(provider: PaymentProvider) -> PaymentInterface:
    providers = injector.get(dict[PaymentProvider, PaymentInterface])
    return providers[provider]


@Result.shield_exception()
def save_payment_event_data(event: PaymentEventData) -> Result[int | None, FatalError]:
    repo = injector.get(PaymentEventInterface)
    filter = PaymentEventFilterOption(provider=event.provider.value, event_id=event.event_id)
    ids_ret = repo.get_ids(filter, PaymentEventSortOption(), PaymentEventPageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) > 0:
        log.info("already recorded", event_id=event.event_id)
        return Result.ok(None)

    save_ret = repo.bulk_save([event])
    if save_ret.is_err:
        saved_ids_ret = repo.get_ids(filter, PaymentEventSortOption(), PaymentEventPageOption(limit=1))
        if saved_ids_ret.is_err:
            return Result.err(saved_ids_ret.err_value)

        saved_ids = saved_ids_ret.ok_value
        if len(saved_ids) > 0:
            log.info("recorded by another request", event_id=event.event_id)
            return Result.ok(None)

        return Result.err(save_ret.err_value)

    new_ids = save_ret.ok_value
    return Result.ok(new_ids[0])


@Result.shield_exception()
def apply_payment_event(event: PaymentEventData) -> Result[None, CommandError]:
    match event.content:
        case ProviderSubscriptionData() as provider_subscription:
            subscription_ret = save_provider_subscription_data(provider_subscription, event.occurred_at)
            if subscription_ret.is_err:
                return Result.err(subscription_ret.err_value)

            return Result.ok(None)
        case PaymentPaidContent() as paid:
            ret = save_payment_data(event, paid)
        case PaymentFailedContent():
            ret = update_transaction_status(event, PaymentStatus.FAILED)
        case RefundContent() as refund:
            ret = record_refund(event, refund)
        case PayoutContent() as payout:
            ret = save_payout_data(event, payout)
        case PurchasePaidContent() as purchase:
            ret = save_purchase_data(event, purchase)
        case _:
            assert_never(event.content)

    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_active_subscription_data(user_id: int) -> Result[SubscriptionData | None, FatalError]:
    repo = injector.get(SubscriptionInterface)
    ids_ret = repo.get_ids(SubscriptionFilterOption(customer_user_id=user_id), SubscriptionSortOption(is_asc=False), SubscriptionPageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    subscriptions_ret = repo.bulk_get(ids)
    if subscriptions_ret.is_err:
        return Result.err(subscriptions_ret.err_value)

    subscriptions = subscriptions_ret.ok_value
    not_canceled_at = datetime.min.replace(tzinfo=timezone.utc)
    active_subscriptions = [s for s in subscriptions if s.status in (SubscriptionStatus.ACTIVE, SubscriptionStatus.PAST_DUE) and s.canceled_at == not_canceled_at]
    if len(active_subscriptions) == 0:
        return Result.ok(None)

    return Result.ok(active_subscriptions[0])


@Result.shield_exception()
def get_payment_seller_data(user_id: int) -> Result[PaymentSellerData | None, FatalError]:
    repo = injector.get(PaymentSellerInterface)
    ids_ret = repo.get_ids(PaymentSellerFilterOption(user_id=user_id), PaymentSellerSortOption(), PaymentSellerPageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    sellers_ret = repo.bulk_get(ids)
    if sellers_ret.is_err:
        return Result.err(sellers_ret.err_value)

    sellers = sellers_ret.ok_value
    if len(sellers) == 0:
        return Result.ok(None)

    return Result.ok(sellers[0])


@Result.shield_exception()
def get_seller_currency_data(user_id: int) -> Result[Currency, AccessError]:
    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    plan = get_plan(user.user_plan.plan) if user is not None else None
    if user is None or plan is None or not plan.is_paid_content:
        log.info("plan required", user_id=user_id)
        return Result.err(ForbiddenError("error.paidContentPlanRequired"))

    seller_ret = get_payment_seller_data(user_id)
    if seller_ret.is_err:
        return Result.err(seller_ret.err_value)

    seller = seller_ret.ok_value
    if seller is None or not seller.is_enabled:
        log.info("seller not enabled", user_id=user_id)
        return Result.err(ForbiddenError("error.sellerNotEnabled"))

    return Result.ok(country_currency(user.profile.country))


@Result.shield_exception()
def get_purchase_ids_data(user_id: int, product_type: ProductType, product_id: int) -> Result[list[int], FatalError]:
    repo = injector.get(PurchaseInterface)
    ids_ret = repo.get_ids(PurchaseFilterOption(user_id=user_id, product_type=product_type, product_ids=[product_id]), PurchaseSortOption(), PurchasePageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    return Result.ok(ids)


@Result.shield_exception()
def get_product_ids_data(product_type: ProductType, ulid: str) -> Result[list[int], FatalError]:
    match product_type:
        case ProductType.BLOG:
            repo = injector.get(BlogInterface)
        case _:
            assert_never(product_type)

    ids_ret = repo.get_ids(MediaFilterOption(ulid=ulid), MediaSortOption(), MediaPageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    return Result.ok(ids)


@Result.shield_exception()
def save_payment_seller_data(data: PaymentSellerData) -> Result[None, FatalError]:
    repo = injector.get(PaymentSellerInterface)
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_subscription_state_data(aggregate_id: str) -> Result[SubscriptionState, HistoryError]:
    repo = injector.get(EventStoreInterface)
    load_ret = repo.load(SUBSCRIPTION_AGGREGATE_TYPE, aggregate_id, 0)
    if load_ret.is_err:
        return Result.err(load_ret.err_value)

    history = load_ret.ok_value
    state_ret = replay(history)
    if state_ret.is_err:
        return Result.err(state_ret.err_value)

    state = state_ret.ok_value
    if state is None:
        return Result.err(FatalError(f"Subscription aggregate not found aggregate_id={aggregate_id}"))

    return Result.ok(state)


@Result.shield_exception()
def save_subscription_event_data(provider_subscription: ProviderSubscriptionData, occurred_at: datetime) -> Result[SubscriptionState, CommandError]:
    repo = injector.get(EventStoreInterface)
    aggregate_id = subscription_aggregate_id(provider_subscription.provider, provider_subscription.external_id)
    command_ret = handle_command(repo, SUBSCRIPTION_AGGREGATE_TYPE, aggregate_id, replay, lambda state: accept_provider_state(state, provider_subscription, occurred_at), occurred_at)
    if command_ret.is_err:
        return Result.err(command_ret.err_value)

    state_ret = get_subscription_state_data(aggregate_id)
    if state_ret.is_err:
        return Result.err(state_ret.err_value)

    state = state_ret.ok_value
    return Result.ok(state)


@Result.shield_exception()
def save_cancellation_request_data(provider: PaymentProvider, external_id: str) -> Result[str, CommandError]:
    repo = injector.get(EventStoreInterface)
    aggregate_id = subscription_aggregate_id(provider, external_id)
    command_ret = handle_command(repo, SUBSCRIPTION_AGGREGATE_TYPE, aggregate_id, replay, request_cancellation, datetime.now(timezone.utc))
    if command_ret.is_err:
        return Result.err(command_ret.err_value)

    state_ret = get_subscription_state_data(aggregate_id)
    if state_ret.is_err:
        return Result.err(state_ret.err_value)

    state = state_ret.ok_value
    if not isinstance(state, ActiveSubscription | PastDueSubscription):
        return Result.err(FatalError(f"Subscription cancellation request not found aggregate_id={aggregate_id}"))

    return Result.ok(state.cancellation_request_id)


@Result.shield_exception()
def save_cancellation_failure_data(provider: PaymentProvider, external_id: str, error: CancelError) -> Result[None, CommandError]:
    repo = injector.get(EventStoreInterface)
    aggregate_id = subscription_aggregate_id(provider, external_id)
    command_ret = handle_command(repo, SUBSCRIPTION_AGGREGATE_TYPE, aggregate_id, replay, lambda state: fail_cancellation(state, error), datetime.now(timezone.utc))
    if command_ret.is_err:
        return Result.err(command_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_provider_subscription_data(provider_subscription: ProviderSubscriptionData, occurred_at: datetime) -> Result[None, CommandError]:
    command_ret = save_subscription_event_data(provider_subscription, occurred_at)
    if command_ret.is_err:
        return Result.err(command_ret.err_value)

    state = command_ret.ok_value
    save_ret = save_subscription_data(state)
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_subscription_data(state: SubscriptionState) -> Result[None, FatalError]:
    detail = state.detail
    if len(detail.user_ulid) == 0:
        log.error("user_ulid missing", external_id=detail.external_id)
        return Result.ok(None)

    user_ret = get_user_data(ulid=detail.user_ulid)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        log.error("not found", external_id=detail.external_id, user_ulid=detail.user_ulid)
        return Result.ok(None)

    repo = injector.get(SubscriptionInterface)
    ids_ret = repo.get_ids(SubscriptionFilterOption(provider=detail.provider.value, external_id=detail.external_id), SubscriptionSortOption(), SubscriptionPageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    customer_ret = save_payment_customer_data(user.user.id, detail.provider, detail.customer_id)
    if customer_ret.is_err:
        return Result.err(customer_ret.err_value)

    customer_id = customer_ret.ok_value
    status = convert_status(state)
    subscription = SubscriptionData(
        id=ids[0] if len(ids) > 0 else 0,
        payment_customer_id=customer_id,
        seller_id="",
        external_id=detail.external_id,
        product_code=detail.product_code,
        price=detail.price,
        status=status,
        started_at=detail.started_at,
        current_period_end=detail.current_period_end,
        canceled_at=detail.canceled_at,
        last_event_at=state.last_occurred_at,
    )
    subscription_ret = repo.bulk_save([subscription])
    if subscription_ret.is_err:
        return Result.err(subscription_ret.err_value)

    user_plan_ret = save_user_plan_data(user, state)
    if user_plan_ret.is_err:
        return Result.err(user_plan_ret.err_value)

    log.info("updated", external_id=detail.external_id, status=status.value)
    return Result.ok(None)


@Result.shield_exception()
def save_user_plan_data(user: UserAllData, state: SubscriptionState) -> Result[None, FatalError]:
    detail = state.detail
    match state:
        case ActiveSubscription() | PastDueSubscription():
            user_plan = replace(
                user.user_plan,
                plan=detail.product_code,
                is_paid=True,
                start_date=detail.started_at,
                end_date=detail.current_period_end,
            )
        case EndedSubscription():
            repo = injector.get(SubscriptionInterface)
            ids_ret = repo.get_ids(SubscriptionFilterOption(customer_user_id=user.user.id), SubscriptionSortOption(), SubscriptionPageOption())
            if ids_ret.is_err:
                return Result.err(ids_ret.err_value)

            ids = ids_ret.ok_value
            subscriptions_ret = repo.bulk_get(ids)
            if subscriptions_ret.is_err:
                return Result.err(subscriptions_ret.err_value)

            subscriptions = subscriptions_ret.ok_value
            active_subscriptions = [s for s in subscriptions if s.status in (SubscriptionStatus.ACTIVE, SubscriptionStatus.PAST_DUE)]
            if len(active_subscriptions) > 0:
                return Result.ok(None)

            user_plan = replace(user.user_plan, plan=PlanName.FREE, is_paid=False, end_date=detail.current_period_end)
        case IncompleteSubscription():
            return Result.ok(None)
        case _:
            assert_never(state)

    ret = save_user_data(replace(user, user_plan=user_plan))
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_payment_data(event: PaymentEventData, paid: PaymentPaidContent) -> Result[None, FatalError]:
    user_ret = get_user_data(ulid=paid.user_ulid)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        log.error("not found", external_id=event.external_id, user_ulid=paid.user_ulid)
        return Result.err(FatalError("Payment user not found"))

    customer_ret = save_payment_customer_data(user.user.id, event.provider, paid.customer_id)
    if customer_ret.is_err:
        return Result.err(customer_ret.err_value)

    customer_id = customer_ret.ok_value
    subscription_id = 0
    if len(paid.subscription_external_id) > 0:
        subscription_repo = injector.get(SubscriptionInterface)
        subscription_ids_ret = subscription_repo.get_ids(SubscriptionFilterOption(provider=event.provider.value, external_id=paid.subscription_external_id), SubscriptionSortOption(), SubscriptionPageOption(limit=1))
        if subscription_ids_ret.is_err:
            return Result.err(subscription_ids_ret.err_value)

        subscription_ids = subscription_ids_ret.ok_value
        if len(subscription_ids) == 0:
            log.warning("subscription not yet recorded", external_id=event.external_id, subscription=paid.subscription_external_id)
            return Result.err(FatalError("Payment subscription not yet recorded"))

        subscription_id = subscription_ids[0]

    transaction_ret = get_transaction_data(event)
    if transaction_ret.is_err:
        return Result.err(transaction_ret.err_value)

    payment_transaction = transaction_ret.ok_value
    if payment_transaction is None or payment_transaction.last_event_at <= event.occurred_at:
        status = PaymentStatus.CAPTURED
        if payment_transaction is not None and payment_status_rank(payment_transaction.status) > payment_status_rank(status):
            status = payment_transaction.status

        transaction = TransactionData(
            id=payment_transaction.id if payment_transaction is not None else 0,
            payment_customer_id=customer_id,
            subscription_id=subscription_id,
            external_id=event.external_id,
            currency=paid.balance.currency,
            tax_rate=TAX_RATE,
            receipt_number=paid.receipt_number,
            status=status,
            paid_at=paid.balance.occurred_at,
            last_event_at=event.occurred_at,
        )
        save_ret = save_transaction_data(transaction)
        if save_ret.is_err:
            return Result.err(save_ret.err_value)

        transaction_id = save_ret.ok_value
        payment_transaction = replace(transaction, id=transaction_id)

    ledger_ret = save_ledger_entry_data(payment_transaction.id, event.id, LedgerEntryType.SALE, [paid.balance])
    if ledger_ret.is_err:
        return Result.err(ledger_ret.err_value)

    log.info("recorded", external_id=event.external_id, amount=paid.balance.amount)
    return Result.ok(None)


@Result.shield_exception()
def save_purchase_data(event: PaymentEventData, purchase: PurchasePaidContent) -> Result[None, FatalError]:
    user_ret = get_user_data(ulid=purchase.user_ulid)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        log.error("not found", external_id=event.external_id, user_ulid=purchase.user_ulid)
        return Result.err(FatalError("Purchase user not found"))

    customer_ret = save_payment_customer_data(user.user.id, event.provider, purchase.customer_id)
    if customer_ret.is_err:
        return Result.err(customer_ret.err_value)

    customer_id = customer_ret.ok_value
    transaction_ret = get_transaction_data(event)
    if transaction_ret.is_err:
        return Result.err(transaction_ret.err_value)

    payment_transaction = transaction_ret.ok_value
    if payment_transaction is None:
        transaction = TransactionData(
            id=0,
            payment_customer_id=customer_id,
            subscription_id=0,
            external_id=event.external_id,
            currency=purchase.balance.currency,
            tax_rate=TAX_RATE,
            receipt_number=purchase.receipt_number,
            status=PaymentStatus.CAPTURED,
            paid_at=purchase.balance.occurred_at,
            last_event_at=event.occurred_at,
        )
        save_ret = save_transaction_data(transaction)
        if save_ret.is_err:
            return Result.err(save_ret.err_value)

        transaction_id = save_ret.ok_value
        payment_transaction = replace(transaction, id=transaction_id)

    sale_ret = save_ledger_entry_data(payment_transaction.id, event.id, LedgerEntryType.SALE, [purchase.balance])
    if sale_ret.is_err:
        return Result.err(sale_ret.err_value)

    transfer_ret = save_ledger_entry_data(payment_transaction.id, event.id, LedgerEntryType.TRANSFER, [purchase.transfer_balance])
    if transfer_ret.is_err:
        return Result.err(transfer_ret.err_value)

    product_type, product_ulid = parse_product_code(purchase.product_code)
    if product_type is None:
        log.error("unknown product", external_id=event.external_id, product_code=purchase.product_code)
        return Result.ok(None)

    product_ids_ret = get_product_ids_data(product_type, product_ulid)
    if product_ids_ret.is_err:
        return Result.err(product_ids_ret.err_value)

    product_ids = product_ids_ret.ok_value
    if len(product_ids) == 0:
        log.error("not found", external_id=event.external_id, product_code=purchase.product_code)
        return Result.ok(None)

    product_id = product_ids[0]
    purchase_ids_ret = get_purchase_ids_data(user.user.id, product_type, product_id)
    if purchase_ids_ret.is_err:
        return Result.err(purchase_ids_ret.err_value)

    purchase_ids = purchase_ids_ret.ok_value
    if len(purchase_ids) == 0:
        repo = injector.get(PurchaseInterface)
        purchase_save_ret = repo.bulk_save([PurchaseData(id=0, user_id=user.user.id, transaction_id=payment_transaction.id, product_type=product_type, product_id=product_id)])
        if purchase_save_ret.is_err:
            return Result.err(purchase_save_ret.err_value)

    log.info("recorded", external_id=event.external_id, amount=purchase.balance.amount, product_code=purchase.product_code)
    return Result.ok(None)


@Result.shield_exception()
def record_refund(event: PaymentEventData, refund: RefundContent) -> Result[None, FatalError]:
    transaction_ret = get_transaction_data(event)
    if transaction_ret.is_err:
        return Result.err(transaction_ret.err_value)

    payment_transaction = transaction_ret.ok_value
    if payment_transaction is None:
        log.warning("transaction not yet recorded", external_id=event.external_id)
        return Result.err(FatalError("Refund transaction not yet recorded"))

    ledger_ret = save_ledger_entry_data(payment_transaction.id, event.id, LedgerEntryType.REFUND, refund.balances)
    if ledger_ret.is_err:
        return Result.err(ledger_ret.err_value)

    reversal_ret = save_ledger_entry_data(payment_transaction.id, event.id, LedgerEntryType.TRANSFER_REVERSAL, refund.transfer_balances)
    if reversal_ret.is_err:
        return Result.err(reversal_ret.err_value)

    status_ret = update_transaction_status(event, PaymentStatus.REFUNDED)
    if status_ret.is_err:
        return Result.err(status_ret.err_value)

    purchase_repo = injector.get(PurchaseInterface)
    purchase_ids_ret = purchase_repo.get_ids(PurchaseFilterOption(transaction_id=payment_transaction.id), PurchaseSortOption(), PurchasePageOption())
    if purchase_ids_ret.is_err:
        return Result.err(purchase_ids_ret.err_value)

    purchase_ids = purchase_ids_ret.ok_value
    purchase_delete_ret = purchase_repo.bulk_delete(purchase_ids)
    if purchase_delete_ret.is_err:
        return Result.err(purchase_delete_ret.err_value)

    log.info("recorded", external_id=event.external_id)
    return Result.ok(None)


@Result.shield_exception()
def save_payout_data(event: PaymentEventData, payout: PayoutContent) -> Result[None, FatalError]:
    repo = injector.get(PayoutInterface)
    ids_ret = repo.get_ids(PayoutFilterOption(provider=event.provider.value, external_id=event.external_id), PayoutSortOption(), PayoutPageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    payouts_ret = repo.bulk_get(ids)
    if payouts_ret.is_err:
        return Result.err(payouts_ret.err_value)

    payouts = payouts_ret.ok_value
    if len(payouts) > 0 and payouts[0].last_event_at > event.occurred_at:
        log.info("event is older than applied", external_id=event.external_id, event_id=event.event_id)
        return Result.ok(None)

    data = PayoutData(
        id=ids[0] if len(ids) > 0 else 0,
        provider=event.provider,
        external_id=event.external_id,
        amount=payout.amount,
        currency=payout.currency,
        status=payout.status,
        arrival_at=payout.arrival_at,
        last_event_at=event.occurred_at,
    )
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    new_ids = save_ret.ok_value
    payout_id = ids[0] if len(ids) > 0 else new_ids[0]

    ledger_repo = injector.get(LedgerEntryInterface)
    entry_ids_ret = ledger_repo.get_ids(LedgerEntryFilterOption(external_ids=payout.balance_external_ids), LedgerEntrySortOption(), LedgerEntryPageOption())
    if entry_ids_ret.is_err:
        return Result.err(entry_ids_ret.err_value)

    entry_ids = entry_ids_ret.ok_value
    entries_ret = ledger_repo.bulk_get(entry_ids)
    if entries_ret.is_err:
        return Result.err(entries_ret.err_value)

    entries = entries_ret.ok_value
    entries_save_ret = ledger_repo.bulk_save([replace(e, payout_id=payout_id) for e in entries])
    if entries_save_ret.is_err:
        return Result.err(entries_save_ret.err_value)

    log.info("recorded", external_id=event.external_id, amount=payout.amount, entries=len(entries))
    return Result.ok(None)


@Result.shield_exception()
def get_transaction_data(event: PaymentEventData) -> Result[TransactionData | None, FatalError]:
    repo = injector.get(TransactionInterface)
    ids_ret = repo.get_ids(TransactionFilterOption(provider=event.provider.value, external_id=event.external_id), TransactionSortOption(), TransactionPageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    transactions_ret = repo.bulk_get(ids)
    if transactions_ret.is_err:
        return Result.err(transactions_ret.err_value)

    transactions = transactions_ret.ok_value
    if len(transactions) == 0:
        return Result.ok(None)

    return Result.ok(transactions[0])


@Result.shield_exception()
def update_transaction_status(event: PaymentEventData, status: PaymentStatus) -> Result[None, FatalError]:
    transaction_ret = get_transaction_data(event)
    if transaction_ret.is_err:
        return Result.err(transaction_ret.err_value)

    payment_transaction = transaction_ret.ok_value
    if payment_transaction is None:
        log.warning("not found", external_id=event.external_id, status=status.value)
        return Result.ok(None)

    if payment_status_rank(status) < payment_status_rank(payment_transaction.status):
        log.info("status not downgraded", external_id=event.external_id, current=payment_transaction.status.value, status=status.value)
        return Result.ok(None)

    if payment_transaction.last_event_at > event.occurred_at:
        log.info("event is older than applied", external_id=event.external_id, event_id=event.event_id)
        return Result.ok(None)

    save_ret = save_transaction_data(replace(payment_transaction, status=status, last_event_at=event.occurred_at))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    log.info("status updated", external_id=event.external_id, status=status.value)
    return Result.ok(None)


@Result.shield_exception()
def save_processed_payment_event_data(event: PaymentEventData) -> Result[None, CommandError]:
    apply_ret = apply_payment_event(event)
    if apply_ret.is_err:
        return Result.err(apply_ret.err_value)

    repo = injector.get(PaymentEventInterface)
    save_ret = repo.bulk_save([replace(event, processed_at=datetime.now(timezone.utc), last_error="")])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_failed_payment_event_data(event: PaymentEventData, error: str) -> Result[None, FatalError]:
    attempts = event.attempts + 1
    repo = injector.get(PaymentEventInterface)
    save_ret = repo.bulk_save([replace(event, attempts=attempts, last_error=error)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if attempts >= PAYMENT_EVENT_MAX_ATTEMPTS:
        log.error("gave up", event_id=event.event_id, event_type=event.event_type.value, attempts=attempts, error=error)
    else:
        log.warning("process failed", event_id=event.event_id, event_type=event.event_type.value, attempts=attempts, error=error)
    return Result.ok(None)


@Result.shield_exception()
def save_payment_customer_data(user_id: int, provider: PaymentProvider, external_id: str) -> Result[int, FatalError]:
    repo = injector.get(PaymentCustomerInterface)
    ids_ret = repo.get_ids(PaymentCustomerFilterOption(user_id=user_id, provider=provider.value), PaymentCustomerSortOption(), PaymentCustomerPageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) > 0:
        return Result.ok(ids[0])

    save_ret = repo.bulk_save([PaymentCustomerData(id=0, user_id=user_id, provider=provider, external_id=external_id)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    new_ids = save_ret.ok_value
    return Result.ok(new_ids[0])


@Result.shield_exception()
def save_transaction_data(data: TransactionData) -> Result[int, FatalError]:
    repo = injector.get(TransactionInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    new_ids = ret.ok_value
    return Result.ok(data.id if data.id != 0 else new_ids[0])


@Result.shield_exception()
def save_ledger_entry_data(transaction_id: int, event_id: int, entry_type: LedgerEntryType, balances: list[BalanceData]) -> Result[None, FatalError]:
    repo = injector.get(LedgerEntryInterface)
    external_ids = [b.external_id for b in balances]
    ids_ret = repo.get_ids(LedgerEntryFilterOption(transaction_id=transaction_id, external_ids=external_ids), LedgerEntrySortOption(), LedgerEntryPageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    entries_ret = repo.bulk_get(ids)
    if entries_ret.is_err:
        return Result.err(entries_ret.err_value)

    entries = entries_ret.ok_value
    recorded = {(e.external_id, e.entry_type) for e in entries}
    new_entries: list[LedgerEntryData] = []
    for balance in balances:
        if (balance.external_id, entry_type) not in recorded:
            new_entries.append(LedgerEntryData(
                id=0,
                transaction_id=transaction_id,
                payout_id=0,
                event_id=event_id,
                external_id=balance.external_id,
                entry_type=entry_type,
                amount=balance.amount,
                tax_amount=included_tax(balance.amount, TAX_RATE),
                occurred_at=balance.occurred_at,
            ))
        if balance.fee != 0 and (balance.external_id, LedgerEntryType.FEE) not in recorded:
            new_entries.append(LedgerEntryData(
                id=0,
                transaction_id=transaction_id,
                payout_id=0,
                event_id=event_id,
                external_id=balance.external_id,
                entry_type=LedgerEntryType.FEE,
                amount=-balance.fee,
                tax_amount=0,
                occurred_at=balance.occurred_at,
            ))

    save_ret = repo.bulk_save(new_entries)
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_payment_projection_data() -> Result[int, CommandError]:
    delete_ret = delete_payment_projection_data()
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    repo = injector.get(PaymentEventInterface)
    ids_ret = repo.get_ids(PaymentEventFilterOption(is_processed=True), PaymentEventSortOption(), PaymentEventPageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    for start in range(0, len(ids), REPLAY_BATCH_SIZE):
        events_ret = repo.bulk_get(ids[start:start + REPLAY_BATCH_SIZE])
        if events_ret.is_err:
            return Result.err(events_ret.err_value)

        events = events_ret.ok_value
        for event in events:
            apply_ret = apply_payment_event(event)
            if apply_ret.is_err:
                log.error("replay failed", event_id=event.event_id, error=apply_ret.err_value.message)
                return Result.err(apply_ret.err_value)

    log.info("replayed", count=len(ids))
    return Result.ok(len(ids))


@Result.shield_exception()
def delete_payment_projection_data() -> Result[None, FatalError]:
    purchase_repo = injector.get(PurchaseInterface)
    purchase_ids_ret = purchase_repo.get_ids(PurchaseFilterOption(), PurchaseSortOption(), PurchasePageOption())
    if purchase_ids_ret.is_err:
        return Result.err(purchase_ids_ret.err_value)

    purchase_ids = purchase_ids_ret.ok_value
    purchase_ret = purchase_repo.bulk_delete(purchase_ids)
    if purchase_ret.is_err:
        return Result.err(purchase_ret.err_value)

    ledger_repo = injector.get(LedgerEntryInterface)
    ledger_ids_ret = ledger_repo.get_ids(LedgerEntryFilterOption(), LedgerEntrySortOption(), LedgerEntryPageOption())
    if ledger_ids_ret.is_err:
        return Result.err(ledger_ids_ret.err_value)

    ledger_ids = ledger_ids_ret.ok_value
    ledger_ret = ledger_repo.bulk_delete(ledger_ids)
    if ledger_ret.is_err:
        return Result.err(ledger_ret.err_value)

    payout_repo = injector.get(PayoutInterface)
    payout_ids_ret = payout_repo.get_ids(PayoutFilterOption(), PayoutSortOption(), PayoutPageOption())
    if payout_ids_ret.is_err:
        return Result.err(payout_ids_ret.err_value)

    payout_ids = payout_ids_ret.ok_value
    payout_ret = payout_repo.bulk_delete(payout_ids)
    if payout_ret.is_err:
        return Result.err(payout_ret.err_value)

    transaction_repo = injector.get(TransactionInterface)
    transaction_ids_ret = transaction_repo.get_ids(TransactionFilterOption(), TransactionSortOption(), TransactionPageOption())
    if transaction_ids_ret.is_err:
        return Result.err(transaction_ids_ret.err_value)

    transaction_ids = transaction_ids_ret.ok_value
    transaction_ret = transaction_repo.bulk_delete(transaction_ids)
    if transaction_ret.is_err:
        return Result.err(transaction_ret.err_value)

    subscription_repo = injector.get(SubscriptionInterface)
    subscription_ids_ret = subscription_repo.get_ids(SubscriptionFilterOption(), SubscriptionSortOption(), SubscriptionPageOption())
    if subscription_ids_ret.is_err:
        return Result.err(subscription_ids_ret.err_value)

    subscription_ids = subscription_ids_ret.ok_value
    subscription_ret = subscription_repo.bulk_delete(subscription_ids)
    if subscription_ret.is_err:
        return Result.err(subscription_ret.err_value)

    return Result.ok(None)
