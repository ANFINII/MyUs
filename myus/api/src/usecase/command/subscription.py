from datetime import datetime
from api.src.domain.aggregate.subscription.apply import replay
from api.src.domain.aggregate.subscription.decide import accept_provider_state
from api.src.domain.aggregate.subscription.event import SUBSCRIPTION_AGGREGATE_TYPE
from api.src.domain.aggregate.subscription.state import SubscriptionState
from api.src.domain.interface.es.interface import EventStoreInterface
from api.src.domain.interface.payment.event.data import ProviderSubscriptionData
from api.src.injectors.container import injector
from api.src.usecase.command.handler import handle_command
from api.utils.common.result import CommandError, FatalError, Result


@Result.shield_exception()
def accept_provider_subscription(provider_subscription: ProviderSubscriptionData, occurred_at: datetime) -> Result[SubscriptionState, CommandError]:
    repo = injector.get(EventStoreInterface)
    aggregate_id = f"{provider_subscription.provider.value}:{provider_subscription.external_id}"
    command_ret = handle_command(repo, SUBSCRIPTION_AGGREGATE_TYPE, aggregate_id, replay, lambda state: accept_provider_state(state, provider_subscription, occurred_at), occurred_at)
    if command_ret.is_err:
        return Result.err(command_ret.err_value)

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
