from django.db import models
from django_quill.fields import QuillField
from django_ulid.models import ulid
from api.db.models.master import Category, HashTag
from api.db.models.base import MediaModel
from api.db.models.user import User
from api.utils.functions.file import image_upload, video_upload, musics_upload, comic_upload


# Video
class Video(models.Model, MediaModel):
    """Video"""
    id       = models.BigAutoField(primary_key=True)
    ulid     = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    image    = models.ImageField(upload_to=image_upload)
    video    = models.FileField(upload_to=video_upload)
    convert  = models.FileField(upload_to=video_upload)
    category = models.ManyToManyField(Category, blank=True)
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name="video_like", blank=True)
    read     = models.IntegerField(default=0)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            image = self.image
            video  = self.video
            convert = self.convert
            self.image = None
            self.video  = None
            self.convert = None
            super().save(*args, **kwargs)
            self.image = image
            self.video  = video
            self.convert = convert
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "video"
        verbose_name_plural = "01 Video"


# Music
class Music(models.Model, MediaModel):
    """Music"""
    id       = models.BigAutoField(primary_key=True)
    ulid     = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    lyric    = models.TextField()
    music    = models.FileField(upload_to=musics_upload)
    category = models.ManyToManyField(Category, blank=True)
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name="music_like", blank=True)
    read     = models.IntegerField(default=0)
    download = models.BooleanField(default=True)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            music = self.music
            self.music = None
            super().save(*args, **kwargs)
            self.music = music
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "music"
        verbose_name_plural = "02 Music"


# Comic
class Comic(models.Model, MediaModel):
    """Comic"""
    id       = models.BigAutoField(primary_key=True)
    ulid     = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    image    = models.ImageField(upload_to=image_upload)
    category = models.ManyToManyField(Category, blank=True)
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name="comic_like", blank=True)
    read     = models.IntegerField(default=0)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            image = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "comic"
        verbose_name_plural = "03 Comic"


class ComicPage(models.Model):
    """ComicPage"""
    id    = models.BigAutoField(primary_key=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name="comic")
    image = models.ImageField(upload_to=comic_upload)
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
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    image    = models.ImageField(upload_to=image_upload)
    category = models.ManyToManyField(Category, blank=True)
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name="picture_like", blank=True)
    read     = models.IntegerField(default=0)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            image = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "picture"
        verbose_name_plural = "04 Picture"


# Blog
class Blog(models.Model, MediaModel):
    """Blog"""
    id       = models.BigAutoField(primary_key=True)
    ulid     = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    richtext = models.TextField()
    delta    = QuillField()
    image    = models.ImageField(upload_to=image_upload)
    category = models.ManyToManyField(Category, blank=True)
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name="blog_like", blank=True)
    read     = models.IntegerField(default=0)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            image = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "blog"
        verbose_name_plural = "05 Blog"


# Chat
class Chat(models.Model):
    """Chat"""
    id       = models.BigAutoField(primary_key=True)
    ulid     = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def thread_count(self):
        return self.message.filter(parent__isnull=True).count()
    thread_count.short_description = "thread"

    def joined_count(self):
        return self.message.values_list("author").distinct().count()
    joined_count.short_description = "joined"

    def score(self):
        return int(self.read + self.like.count()*10 + self.read*self.like.count()/(self.read+1)*20)

    class Meta:
        db_table = "chat"
        verbose_name_plural = "06 Chat"
