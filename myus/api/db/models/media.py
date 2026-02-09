from django.db import models
from django_quill.fields import QuillField
from django_ulid.models import ulid
from api.db.models.base import MediaModel
from api.db.models.channel import Channel
from api.db.models.master import Category, HashTag
from api.db.models.user import User
from api.utils.functions.file import comic_upload, image_upload, music_upload, video_upload


# Video
class Video(models.Model, MediaModel):
    """Video"""
    id       = models.BigAutoField(primary_key=True)
    ulid     = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    channel  = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="videos")
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    image    = models.ImageField(upload_to=image_upload, blank=True)
    video    = models.FileField(upload_to=video_upload, blank=True)
    convert  = models.FileField(upload_to=video_upload, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name="video_like", blank=True)
    read     = models.IntegerField(default=0)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "video"
        verbose_name_plural = "01 Video"


# Music
class Music(models.Model, MediaModel):
    """Music"""
    id       = models.BigAutoField(primary_key=True)
    ulid     = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    channel  = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="musics")
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    lyric    = models.TextField()
    music    = models.FileField(upload_to=music_upload, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name="music_like", blank=True)
    read     = models.IntegerField(default=0)
    download = models.BooleanField(default=True)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "music"
        verbose_name_plural = "02 Music"


# Comic
class Comic(models.Model, MediaModel):
    """Comic"""
    id       = models.BigAutoField(primary_key=True)
    ulid     = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    channel  = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="comics")
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    image    = models.ImageField(upload_to=image_upload, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name="comic_like", blank=True)
    read     = models.IntegerField(default=0)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comic"
        verbose_name_plural = "03 Comic"


class ComicPage(models.Model):
    """ComicPage"""
    id    = models.BigAutoField(primary_key=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name="comic")
    image = models.ImageField(upload_to=comic_upload, blank=True)
    sequence = models.IntegerField(default=0)

    class Meta:
        db_table = "comic_page"
        verbose_name_plural = "03 ComicPage"
        constraints = [
            models.UniqueConstraint(fields=["comic", "sequence"], name="lesson_unique")
        ]

# Picture
class Picture(models.Model, MediaModel):
    """Picture"""
    id       = models.BigAutoField(primary_key=True)
    ulid     = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    channel  = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="pictures")
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    image    = models.ImageField(upload_to=image_upload, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name="picture_like", blank=True)
    read     = models.IntegerField(default=0)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "picture"
        verbose_name_plural = "04 Picture"


# Blog
class Blog(models.Model, MediaModel):
    """Blog"""
    id       = models.BigAutoField(primary_key=True)
    ulid     = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    channel  = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="blogs")
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    richtext = models.TextField()
    delta    = QuillField()
    image    = models.ImageField(upload_to=image_upload, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name="blog_like", blank=True)
    read     = models.IntegerField(default=0)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blog"
        verbose_name_plural = "05 Blog"


# Chat
class Chat(models.Model):
    """Chat"""
    id       = models.BigAutoField(primary_key=True)
    ulid     = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    channel  = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="chats")
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    category = models.ManyToManyField(Category, blank=True)
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name="chat_like", blank=True)
    read     = models.IntegerField(default=0)
    period   = models.DateField()
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def total_like(self):
        return self.like.count()
    total_like.short_description = "like"

    def thread_count(self) -> int:
        return self.message.filter(parent__isnull=True).count()
    thread_count.short_description = "thread"

    def joined_count(self) -> int:
        return self.message.values_list("author").distinct().count()
    joined_count.short_description = "joined"

    def score(self):
        return int(self.read + self.like.count()*10 + self.read*self.like.count()/(self.read+1)*20)

    class Meta:
        db_table = "chat"
        verbose_name_plural = "06 Chat"
