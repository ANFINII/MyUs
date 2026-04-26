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
    video    = models.ForeignKey("db.Video", on_delete=models.CASCADE, related_name="video_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="video_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "video_hashtag"
        unique_together = [("video", "hashtag")]
        ordering = ["sequence"]


class MusicHashtag(models.Model):
    """MusicHashtag"""
    id       = models.BigAutoField(primary_key=True)
    music    = models.ForeignKey("db.Music", on_delete=models.CASCADE, related_name="music_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="music_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "music_hashtag"
        unique_together = [("music", "hashtag")]
        ordering = ["sequence"]


class BlogHashtag(models.Model):
    """BlogHashtag"""
    id       = models.BigAutoField(primary_key=True)
    blog     = models.ForeignKey("db.Blog", on_delete=models.CASCADE, related_name="blog_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="blog_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "blog_hashtag"
        unique_together = [("blog", "hashtag")]
        ordering = ["sequence"]


class ComicHashtag(models.Model):
    """ComicHashtag"""
    id       = models.BigAutoField(primary_key=True)
    comic    = models.ForeignKey("db.Comic", on_delete=models.CASCADE, related_name="comic_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="comic_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "comic_hashtag"
        unique_together = [("comic", "hashtag")]
        ordering = ["sequence"]


class PictureHashtag(models.Model):
    """PictureHashtag"""
    id       = models.BigAutoField(primary_key=True)
    picture  = models.ForeignKey("db.Picture", on_delete=models.CASCADE, related_name="picture_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="picture_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "picture_hashtag"
        unique_together = [("picture", "hashtag")]
        ordering = ["sequence"]


class ChatHashtag(models.Model):
    """ChatHashtag"""
    id       = models.BigAutoField(primary_key=True)
    chat     = models.ForeignKey("db.Chat", on_delete=models.CASCADE, related_name="chat_hashtags")
    hashtag  = models.ForeignKey(HashTag, on_delete=models.CASCADE, related_name="chat_hashtags")
    sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "chat_hashtag"
        unique_together = [("chat", "hashtag")]
        ordering = ["sequence"]
