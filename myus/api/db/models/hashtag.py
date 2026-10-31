from django.db import models
from django_ulid.models import ulid


class HashTag(models.Model):
    """HashTag"""
    id   = models.BigAutoField(primary_key=True)
    ulid = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "hashtag"
        verbose_name_plural = "001 ハッシュタグ"


class VideoHashtag(models.Model):
    """VideoHashtag"""
    id       = models.BigAutoField(primary_key=True)
    video    = models.ForeignKey("myus.Video", on_delete=models.CASCADE, related_name="video_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="video_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "video_hashtag"
        constraints = [
            models.UniqueConstraint(fields=["video", "hashtag"], name="video_hashtag_uniq"),
        ]
        ordering = ["sequence"]


class MusicHashtag(models.Model):
    """MusicHashtag"""
    id       = models.BigAutoField(primary_key=True)
    music    = models.ForeignKey("myus.Music", on_delete=models.CASCADE, related_name="music_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="music_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "music_hashtag"
        constraints = [
            models.UniqueConstraint(fields=["music", "hashtag"], name="music_hashtag_uniq"),
        ]
        ordering = ["sequence"]


class BlogHashtag(models.Model):
    """BlogHashtag"""
    id       = models.BigAutoField(primary_key=True)
    blog     = models.ForeignKey("myus.Blog", on_delete=models.CASCADE, related_name="blog_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="blog_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "blog_hashtag"
        constraints = [
            models.UniqueConstraint(fields=["blog", "hashtag"], name="blog_hashtag_uniq"),
        ]
        ordering = ["sequence"]


class ComicHashtag(models.Model):
    """ComicHashtag"""
    id       = models.BigAutoField(primary_key=True)
    comic    = models.ForeignKey("myus.Comic", on_delete=models.CASCADE, related_name="comic_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="comic_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "comic_hashtag"
        constraints = [
            models.UniqueConstraint(fields=["comic", "hashtag"], name="comic_hashtag_uniq"),
        ]
        ordering = ["sequence"]


class PictureHashtag(models.Model):
    """PictureHashtag"""
    id       = models.BigAutoField(primary_key=True)
    picture  = models.ForeignKey("myus.Picture", on_delete=models.CASCADE, related_name="picture_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="picture_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "picture_hashtag"
        constraints = [
            models.UniqueConstraint(fields=["picture", "hashtag"], name="picture_hashtag_uniq"),
        ]
        ordering = ["sequence"]


class ChatHashtag(models.Model):
    """ChatHashtag"""
    id       = models.BigAutoField(primary_key=True)
    chat     = models.ForeignKey("myus.Chat", on_delete=models.CASCADE, related_name="chat_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="chat_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "chat_hashtag"
        constraints = [
            models.UniqueConstraint(fields=["chat", "hashtag"], name="chat_hashtag_uniq"),
        ]
        ordering = ["sequence"]
