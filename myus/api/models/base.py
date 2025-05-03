class MediaModel:
    def __str__(self):
        return self.title

    def total_like(self):
        return self.like.count()
    total_like.short_description = "like"

    def comment_count(self):
        return 1
    comment_count.short_description = "comment"

    def score(self):
        return int(self.read + self.like.count()*10 + self.read*self.like.count()/(self.read+1)*20)


class MediaManager:
    def search(self, query=None):
        return self.get_queryset().search(query=query)
