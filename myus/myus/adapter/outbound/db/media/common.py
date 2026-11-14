from datetime import timedelta
from typing import TypeVar, cast
from django.db.models import Case, Count, Exists, ExpressionWrapper, F, FloatField, Func, Model, OuterRef, Q, Value, When
from django.db.models.functions import Now
from django.db.models.query import QuerySet
from django.utils import timezone
from myus.db.models.subscribe import Subscribe
from myus.domain.media.common import FilterOption, PageOption, SortOption, SortType


RECOMMEND_DAYS = 200
SUBSCRIBE_BOOST = 2.0

T = TypeVar("T", bound=Model)


class DaysSince(Func):
    function = "TIMESTAMPDIFF"
    template = "(TIMESTAMPDIFF(DAY, %(expressions)s) + 1)"


def filter_recommend() -> Q:
    return Q(created__gte=timezone.now() - timedelta(days=RECOMMEND_DAYS), like__isnull=False)


def filter_search(search: str) -> Q:
    return Q(title__icontains=search) | Q(hashtag__name=search)


def filter_q_list(filter: FilterOption) -> list[Q]:
    q_list: list[Q] = []
    if filter.ulid:
        q_list.append(Q(ulid=filter.ulid))
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
        q_list.append(Q(category__id=filter.category_id))
    if filter.is_recommend:
        q_list.append(filter_recommend())
    if filter.search:
        q_list.append(filter_search(filter.search))
    if filter.exclude_id:
        q_list.append(~Q(id=filter.exclude_id))
    return q_list


def distinct_queryset(qs: QuerySet[T], filter: FilterOption) -> QuerySet[T]:
    if filter.search or filter.is_recommend or filter.category_id:
        return qs.distinct()
    return qs


def sort_queryset(qs: QuerySet[T], sort: SortOption, is_recommend: bool = False) -> QuerySet[T]:
    if sort.sort_type == SortType.SCORE:
        like_count = Count("like", distinct=True)
        if is_recommend:
            days_since = DaysSince(F("created"), Now(), output_field=FloatField())
            score_expr = ExpressionWrapper(like_count * 1000.0 / (F("read") + 1) / days_since, output_field=FloatField())
        else:
            base = F("read") + like_count * 10 + F("read") * like_count / (F("read") + 1) * 20
            user_id = sort.user_id
            if user_id is not None:
                is_subscribed = Exists(Subscribe.objects.filter(user_id=user_id, channel=OuterRef("channel"), is_subscribe=True))
                multiplier = Case(When(is_subscribed, then=Value(SUBSCRIBE_BOOST)), default=Value(1.0), output_field=FloatField())
                score_expr = ExpressionWrapper(base * multiplier, output_field=FloatField())
            else:
                score_expr = ExpressionWrapper(base, output_field=FloatField())
        qs = cast(QuerySet[T], qs.annotate(score=score_expr))
        key = "score"
    else:
        key = sort.sort_type.name.lower()

    order_by_key = key if sort.is_asc else f"-{key}"
    return qs.order_by(order_by_key)


def get_ids_queryset(qs: QuerySet[T], filter: FilterOption, sort: SortOption, page: PageOption) -> QuerySet[T]:
    qs = qs.filter(*filter_q_list(filter))
    qs = distinct_queryset(qs, filter)
    qs = sort_queryset(qs, sort, filter.is_recommend)
    return qs[page.offset:page.offset + page.limit]
