from datetime import timedelta
from typing import TypeVar
from django.db.models import Count, ExpressionWrapper, F, FloatField, Func, Model, Q
from django.db.models.functions import Now
from django.db.models.query import QuerySet
from django.utils import timezone
from api.src.domain.interface.media.index import RECOMMEND_DAYS, SortOption, SortType

T = TypeVar("T", bound=Model)


class DaysSince(Func):
    function = "TIMESTAMPDIFF"
    template = "(TIMESTAMPDIFF(DAY, %(expressions)s) + 1)"
    output_field = FloatField()


def filter_recommend() -> Q:
    return Q(created__gte=timezone.now() - timedelta(days=RECOMMEND_DAYS), like__isnull=False)


def filter_search(search: str) -> Q:
    return Q(title__icontains=search) | Q(hashtag__jp_name=search)


def sort_queryset(qs: QuerySet[T], sort: SortOption, is_recommend: bool = False) -> tuple[QuerySet[T], str]:
    if sort.sort_type == SortType.SCORE:
        like_count = Count("like")
        if is_recommend:
            days_since = DaysSince(F("created"), Now())
            qs = qs.annotate(
                score=ExpressionWrapper(like_count * 1000.0 / (F("read") + 1) / days_since, output_field=FloatField()),
            )
        else:
            qs = qs.annotate(
                score=ExpressionWrapper(F("read") + like_count * 10 + F("read") * like_count / (F("read") + 1) * 20, output_field=FloatField()),
            )
        order_by_key = "score" if sort.is_asc else "-score"
    else:
        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
    return qs, order_by_key
