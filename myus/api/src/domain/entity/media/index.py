from datetime import timedelta
from typing import TypeVar
from django.db.models import Case, Count, Exists, ExpressionWrapper, F, FloatField, Func, Model, OuterRef, Q, Value, When
from django.db.models.functions import Now
from django.db.models.query import QuerySet
from django.utils import timezone
from api.db.models.subscribe import Subscribe
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, RECOMMEND_DAYS, SortOption, SortType, SUBSCRIBE_BOOST

T = TypeVar("T", bound=Model)


class DaysSince(Func):
    function = "TIMESTAMPDIFF"
    template = "(TIMESTAMPDIFF(DAY, %(expressions)s) + 1)"
    output_field = FloatField()


def filter_recommend() -> Q:
    return Q(created__gte=timezone.now() - timedelta(days=RECOMMEND_DAYS), like__isnull=False)


def filter_search(search: str) -> Q:
    return Q(title__icontains=search) | Q(hashtag__jp_name=search)


def filter_q_list(filter: FilterOption, exclude: ExcludeOption | None = None) -> list[Q]:
    q_list: list[Q] = []
    if filter.ulid:
        q_list.append(Q(ulid=filter.ulid))
    if filter.publish is not None:
        q_list.append(Q(publish=filter.publish))
    if filter.owner_id:
        q_list.append(Q(channel__owner_id=filter.owner_id))
    if filter.channel_id:
        q_list.append(Q(channel_id=filter.channel_id))
    if filter.category_id:
        q_list.append(Q(category__id=filter.category_id))
    if filter.is_recommend:
        q_list.append(filter_recommend())
    if filter.search:
        q_list.append(filter_search(filter.search))
    if exclude and exclude.id:
        q_list.append(~Q(id=exclude.id))
    return q_list


def distinct_queryset(qs: QuerySet[T], filter: FilterOption) -> QuerySet[T]:
    if filter.search or filter.is_recommend or filter.category_id:
        return qs.distinct()
    return qs


def sort_queryset(qs: QuerySet[T], sort: SortOption, is_recommend: bool = False, user_id: int | None = None) -> tuple[QuerySet[T], str]:
    if sort.sort_type == SortType.SCORE:
        like_count = Count("like")
        if is_recommend:
            days_since = DaysSince(F("created"), Now())
            score_expr = ExpressionWrapper(like_count * 1000.0 / (F("read") + 1) / days_since, output_field=FloatField())
        else:
            base = F("read") + like_count * 10 + F("read") * like_count / (F("read") + 1) * 20
            if user_id is not None:
                is_subscribed = Exists(Subscribe.objects.filter(user_id=user_id, channel=OuterRef("channel"), is_subscribe=True))
                multiplier = Case(When(is_subscribed, then=Value(SUBSCRIBE_BOOST)), default=Value(1.0), output_field=FloatField())
                score_expr = ExpressionWrapper(base * multiplier, output_field=FloatField())
            else:
                score_expr = ExpressionWrapper(base, output_field=FloatField())
        qs = qs.annotate(score=score_expr)
        key = "score"
    else:
        key = sort.sort_type.name.lower()

    order_by_key = key if sort.is_asc else f"-{key}"
    return qs, order_by_key
