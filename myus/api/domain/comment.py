from dataclasses import dataclass
from enum import Enum, auto
from django.db.models import Exists, OuterRef, Prefetch
from api.models.comment import Comment



class CommnetDomain:
    @staticmethod
    def get(media_type: str, object_id: int, author_id: int) -> list[Comment]:
        filter_obj = dict(media_type=media_type, object_id=object_id)
        subquery = Comment.objects.filter(id=OuterRef("pk"), like__id=author_id, **filter_obj)

        objs = (
            Comment.objects
            .filter(parent__isnull=True, **filter_obj)
            .prefetch_related(Prefetch("reply", queryset=Comment.objects.select_related("author")))
            .select_related("author")
            .annotate(is_comment_like=Exists(subquery))
        )

        return objs
