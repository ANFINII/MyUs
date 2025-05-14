from api.models.comment import Comment

class MediaModel:
    def __str__(self):
        return self.title

    def total_like(self):
        return self.like.count()
    total_like.short_description = "like"

    def comment_count(self):
        class_name = self.__class__.__name__
        objs = Comment.objects.filter(media_type=class_name, object_id=self.id).count()
        count = objs.count()
        return count
    comment_count.short_description = "comment"

    def score(self):
        return int(self.read + self.like.count()*10 + self.read*self.like.count()/(self.read+1)*20)


class MediaManager:
    def search(self, query=None):
        return self.get_queryset().search(query=query)
