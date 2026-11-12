from typing import Any
from django.contrib import admin
from myus.utils.enum.media import CommentType
from myus.utils.functions.map import comment_type_no_map
from .comment import Comment


class MediaModel:
    id: int
    title: str
    read: int
    like: Any

    def __str__(self) -> str:
        return self.title

    @admin.display(description="like")
    def total_like(self) -> int:
        return int(self.like.count())

    @admin.display(description="comment")
    def comment_count(self) -> int:
        class_name = self.__class__.__name__
        type_no = comment_type_no_map(CommentType(class_name))
        objs = Comment.objects.filter(type_no=type_no, object_id=self.id)
        return objs.count()

    def score(self) -> int:
        return int(self.read + self.like.count()*10 + self.read*self.like.count()/(self.read+1)*20)
