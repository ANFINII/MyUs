from api.db.models.comment import Comment
from api.utils.enum.index import CommentType
from api.utils.functions.map import comment_type_no_map


class MediaModel:
    def __str__(self):
        return self.title

    def total_like(self):
        return self.like.count()
    total_like.short_description = "like"

    def comment_count(self) -> int:
        class_name = self.__class__.__name__
        type_no = comment_type_no_map(CommentType(class_name))
        objs = Comment.objects.filter(type_no=type_no, object_id=self.id)
        return objs.count()
    comment_count.short_description = "comment"

    def score(self):
        return int(self.read + self.like.count()*10 + self.read*self.like.count()/(self.read+1)*20)
