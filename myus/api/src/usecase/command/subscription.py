from datetime import datetime
from api.modules.logger import log
from api.src.domain.aggregate.subscription.apply import replay
from api.src.domain.aggregate.subscription.decide import accept_provider_state
from api.src.domain.aggregate.subscription.event import SUBSCRIPTION_AGGREGATE_TYPE
from api.src.domain.interface.es.interface import EventStoreInterface
from api.src.domain.interface.es.subscription_lookup.data import SubscriptionLookupData
from api.src.domain.interface.es.subscription_lookup.interface import FilterOption, SortOption, SubscriptionLookupInterface
from api.src.domain.interface.payment.event.data import ProviderSubscriptionData
from api.src.injectors.container import injector
from api.src.usecase.command.handler import handle_command
from api.utils.common.result import CommandError, Result
from api.utils.functions.index import new_ulid
from api.utils.functions.transaction import atomic_result


@Result.shield_exception()
def accept_provider_subscription(provider_subscription: ProviderSubscriptionData, occurred_at: datetime) -> Result[None, CommandError]:
    return atomic_result(lambda: save_provider_subscription_data(provider_subscription, occurred_at))


@Result.shield_exception()
def save_provider_subscription_data(provider_subscription: ProviderSubscriptionData, occurred_at: datetime) -> Result[None, CommandError]:
    lookup_repo = injector.get(SubscriptionLookupInterface)
    ids_ret = lookup_repo.get_ids(FilterOption(provider=provider_subscription.provider.value, external_id=provider_subscription.external_id), SortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    lookups_ret = lookup_repo.bulk_get(ids)
    if lookups_ret.is_err:
        return Result.err(lookups_ret.err_value)

    lookups = lookups_ret.ok_value
    aggregate_id = lookups[0].aggregate_id if len(lookups) > 0 else new_ulid()
    repo = injector.get(EventStoreInterface)
    command_ret = handle_command(repo, SUBSCRIPTION_AGGREGATE_TYPE, aggregate_id, replay, lambda state: accept_provider_state(state, provider_subscription, occurred_at), occurred_at)
    if command_ret.is_err:
        return Result.err(command_ret.err_value)

    envelopes = command_ret.ok_value
    if len(lookups) > 0 or len(envelopes) == 0:
        return Result.ok(None)

    lookup = SubscriptionLookupData(id=0, aggregate_id=aggregate_id, provider=provider_subscription.provider, external_id=provider_subscription.external_id)
    save_ret = lookup_repo.bulk_save([lookup])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    log.info("Subscription aggregate opened", aggregate_id=aggregate_id, external_id=provider_subscription.external_id)
    return Result.ok(None)
