from datetime import timedelta
from typing import TypeVar, cast
from django.db.models import Case, Count, Exists, ExpressionWrapper, F, FloatField, Func, Model, OuterRef, Q, Value, When
from django.db.models.expressions import CombinedExpression
from django.db.models.functions import Now
from django.db.models.query import QuerySet
from django.utils import timezone
from myus.db.models.subscribe import Subscribe
from myus.domain.media.common import FilterOption, PageOption, SortOption, SortType
from ..common import page_queryset


RECOMMEND_DAYS = 200
SUBSCRIBE_BOOST = 2.0

T = TypeVar("T", bound=Model)


class DaysSince(Func):
    template = "(TIMESTAMPDIFF(DAY, %(expressions)s) + 1)"


def filter_recommend(model: type[Model]) -> Q:
    liked_ids = model._default_manager.filter(like__isnull=False).values("id")
    return Q(created__gte=timezone.now() - timedelta(days=RECOMMEND_DAYS), id__in=liked_ids)


def filter_search(model: type[Model], search: str) -> Q:
    tagged_ids = model._default_manager.filter(hashtag__name=search).values("id")
    return Q(title__icontains=search) | Q(id__in=tagged_ids)


def filter_category(model: type[Model], category_id: int) -> Q:
    categorized_ids = model._default_manager.filter(category__id=category_id).values("id")
    return Q(id__in=categorized_ids)


def filter_q_list(model: type[Model], filter: FilterOption) -> list[Q]:
    q_list: list[Q] = []
    if filter.ulid:
        q_list.append(Q(ulid=filter.ulid))
    if len(filter.ids) > 0:
        q_list.append(Q(id__in=filter.ids))
    if len(filter.ulids) > 0:
        q_list.append(Q(ulid__in=filter.ulids))
    if filter.publish is not None:
        q_list.append(Q(publish=filter.publish))
    if filter.publish:
        q_list.append(Q(publish_at__lte=Now()))
    if filter.owner_id:
        q_list.append(Q(channel__owner_id=filter.owner_id))
    if filter.channel_id:
        q_list.append(Q(channel_id=filter.channel_id))
    if filter.channel_ulid:
        q_list.append(Q(channel__ulid=filter.channel_ulid))
    if filter.category_id:
        q_list.append(filter_category(model, filter.category_id))
    if filter.is_recommend:
        q_list.append(filter_recommend(model))
    if filter.search:
        q_list.append(filter_search(model, filter.search))
    if filter.exclude_id:
        q_list.append(~Q(id=filter.exclude_id))
    return q_list


def filter_queryset(qs: QuerySet[T], filter: FilterOption) -> QuerySet[T]:
    return qs.filter(*filter_q_list(qs.model, filter))


def score_expression(sort: SortOption, is_recommend: bool) -> CombinedExpression:
    like_count = Count("like", distinct=True)
    if is_recommend:
        days_since = DaysSince(F("created"), Now(), output_field=FloatField())
        return like_count * 1000.0 / (F("read") + 1) / days_since

    base = F("read") + like_count * 10 + F("read") * like_count / (F("read") + 1) * 20
    user_id = sort.user_id
    if user_id is None:
        return base

    is_subscribed = Exists(Subscribe.objects.filter(user_id=user_id, channel=OuterRef("channel"), is_subscribe=True))
    multiplier = Case(When(is_subscribed, then=Value(SUBSCRIBE_BOOST)), default=Value(1.0), output_field=FloatField())
    return base * multiplier


def sort_queryset(qs: QuerySet[T], sort: SortOption, is_recommend: bool = False) -> QuerySet[T]:
    if sort.sort_type == SortType.SCORE:
        score = ExpressionWrapper(score_expression(sort, is_recommend), output_field=FloatField())
        qs = cast(QuerySet[T], qs.annotate(score=score))
        key = "score"
    else:
        key = sort.sort_type.name.lower()

    keys = [key] if key == "id" else [key, "id"]
    order_by_keys = [k if sort.is_asc else f"-{k}" for k in keys]
    return qs.order_by(*order_by_keys)


def get_ids_queryset(qs: QuerySet[T], filter: FilterOption, sort: SortOption, page: PageOption) -> QuerySet[T]:
    qs = filter_queryset(qs, filter)
    qs = sort_queryset(qs, sort, filter.is_recommend)
    return page_queryset(qs, page)
