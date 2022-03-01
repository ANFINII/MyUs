from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.mail import send_mail
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
import datetime

# Create your models here.

class UserManager(BaseUserManager):
    """UserManager"""
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')
        elif not email:
            raise ValueError('Users must have an email')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nickname, email, password, **extra_fields):
        user = self.create_user(username, nickname=nickname, email=self.normalize_email(email), password=password)
        user.is_premium = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def user_image_path(instance, filename):
    return f'users/images_user/user_{instance.id}/{filename}'

class User(AbstractBaseUser, PermissionsMixin):
    """CustomUserModel"""
    user_image    = models.ImageField(upload_to=user_image_path, default='../static/img/user_icon.png', blank=True, null=True)
    email         = models.EmailField(max_length=255, unique=True, db_index=True)
    username      = models.CharField(max_length=20, unique=True, db_index=True)
    nickname      = models.CharField(max_length=80, unique=True, db_index=True)
    last_name     = models.CharField(max_length=40, blank=True)
    first_name    = models.CharField(max_length=40, blank=True)

    birthday      = models.DateField(blank=True, null=True)
    gender_choice = (('0', '男性'), ('1', '女性'), ('2', '秘密'))
    gender        = models.CharField(choices=gender_choice, max_length=1, default='2')
    phone_no      = RegexValidator(regex=r'\d{2,4}-?\d{2,4}-?\d{3,4}', message = ('電話番号は090-1234-5678の形式で入力する必要があります。最大15桁まで入力できます。'))
    phone         = models.CharField(validators=[phone_no], max_length=15, blank=True, default='000-0000-0000')
    location      = models.CharField(max_length=255, blank=True)
    introduction  = models.TextField(blank=True)

    is_active     = models.BooleanField(default=True)
    is_staff      = models.BooleanField(default=False)
    is_admin      = models.BooleanField(default=False)
    last_login    = models.DateTimeField(auto_now_add=True)
    date_joined   = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['username', 'email']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_username(self):
        return self.nickname

    def get_fullname(self):
        return self.last_name + ' ' + self.first_name

    def get_year(self):
        if self.birthday is not None:
            return self.birthday.year

    def get_month(self):
        if self.birthday is not None:
            return self.birthday.month

    def get_day(self):
        if self.birthday is not None:
            return self.birthday.day

    def get_age(self):
        if self.birthday is not None:
            DAYS_IN_YEAR = 365.2425
            return int((datetime.date.today() - self.birthday).days / DAYS_IN_YEAR)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        if self.id is None:
            user_image = self.user_image
            self.user_image = None
            super().save(*args, **kwargs)
            self.user_image = user_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '00 User'

@property
def image_url(self):
    if self.user_image and hasattr(self.user_image, 'url'):
        return self.user_image.url


def mypage_image_path(instance, filename):
    return f'users/images_mypage/user_{instance.id}/{filename}'

class MyPage(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    mypage_image    = models.ImageField(upload_to=mypage_image_path, default='../static/img/MyUs_banner.png', blank=True, null=True)
    mypage_email    = models.EmailField(max_length=120, blank=True, null=True, default='abc@gmail.com')
    content         = models.TextField(blank=True)
    follower_count  = models.IntegerField(verbose_name='follower', blank=True, null=True, default=0)
    following_count = models.IntegerField(verbose_name='follow', blank=True, null=True, default=0)
    plan_choice     = (('0', 'Free'), ('1', 'Basic'), ('2', 'Standard'), ('3', 'Premium'))
    rate_plan       = models.CharField(choices=plan_choice, max_length=1, default='0')
    rate_plan_date  = models.DateTimeField(blank=True, null=True)
    auto_advertise  = models.BooleanField(default=True)

    def __str__(self):
        return self.user.nickname

    def get_following_count(self):
        self.following_count = FollowModel.objects.filter(follower=User.id).count()
        return self.following_count

    def get_follower_count(self):
        self.follower_count = FollowModel.objects.filter(following=User.id).count()
        return self.follower_count

    def save(self, *args, **kwargs):
        if self.id is None:
            mypage_image = self.mypage_image
            self.mypage_image = None
            super().save(*args, **kwargs)
            self.mypage_image = mypage_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '00 MyPage'

@property
def mypage_image(self):
    if self.mypage_image and hasattr(self.mypage_image, 'url'):
        return self.mypage_image.url

@receiver(post_save, sender=User)
def create_mypage(sender, **kwargs):
    """ユーザー作成時に空のMyPageも作成する"""
    if kwargs['created']:
        MyPage.objects.get_or_create(owner=kwargs['instance'])


class NotifySettingModel(models.Model):
    """NotifySettingModel"""
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    video   = models.BooleanField(default=False)
    live    = models.BooleanField(default=False)
    music   = models.BooleanField(default=False)
    picture = models.BooleanField(default=False)
    blog    = models.BooleanField(default=False)
    chat    = models.BooleanField(default=False)
    collabo = models.BooleanField(default=False)
    follow  = models.BooleanField(default=True)
    reply   = models.BooleanField(default=True)
    like    = models.BooleanField(default=True)
    views   = models.BooleanField(default=True)

    def __str__(self):
        return self.user.nickname

    class Meta:
        verbose_name_plural = '00 通知設定'

@receiver(post_save, sender=User)
def create_notify_setting(sender, **kwargs):
    """ユーザー作成時に空のnotify_settingも作成する"""
    if kwargs['created']:
        NotifySettingModel.objects.get_or_create(owner=kwargs['instance'])


class SearchTagModel(models.Model):
    """SearchTagModel"""
    author    = models.ForeignKey(User, on_delete=models.CASCADE)
    sequence  = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], default=20)
    searchtag = models.CharField(max_length=30, null=True)
    created   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.searchtag

    class Meta:
        verbose_name_plural = '09 検索タグ'


class TagModel(models.Model):
    """TagModel"""
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    tag         = models.CharField(max_length=30, null=True)
    english_tag = models.CharField(max_length=60, null=True)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name_plural = '10 ハッシュタグ'


class VideoQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) |
                Q(tags__tag__icontains=query) |
                Q(author__nickname__icontains=query) |
                Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

def images_video_upload_path(instance, filename):
    return f'images/images_video/user_{instance.author.id}/object_{instance.id}/{filename}'

def videos_video_upload_path(instance, filename):
    return f'videos/videos_video/user_{instance.author.id}/object_{instance.id}/{filename}'

class VideoModel(models.Model):
    """VideoModel"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    images   = models.ImageField(upload_to=images_video_upload_path)
    videos   = models.FileField(upload_to=videos_video_upload_path)
    convert  = models.FileField(upload_to=videos_video_upload_path)
    comments = GenericRelation('CommentModel')
    publish  = models.BooleanField(default=True)
    tags     = models.ManyToManyField(TagModel, blank=True)
    like     = models.ManyToManyField(User, related_name='video_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    objects  = VideoManager()

    def __str__(self):
        return self.title

    def score(self):
        return self.read + self.like.count()*10 + self.read*self.like.count()/self.read*20

    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.filter(parent__isnull=True).count()

    def save(self, *args, **kwargs):
        if self.id is None:
            images = self.images
            videos = self.videos
            convert = self.convert
            self.images = None
            self.videos = None
            self.convert = None
            super().save(*args, **kwargs)
            self.images = images
            self.videos = videos
            self.convert = convert
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '01 Video'


class LiveQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) |
                Q(tags__tag__icontains=query) |
                Q(author__nickname__icontains=query) |
                Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class LiveManager(models.Manager):
    def get_queryset(self):
        return LiveQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

def images_live_upload_path(instance, filename):
    return f'images/images_live/user_{instance.author.id}/object_{instance.id}/{filename}'

def videos_live_upload_path(instance, filename):
    return f'videos/videos_live/user_{instance.author.id}/object_{instance.id}/{filename}'

class LiveModel(models.Model):
    """LiveModel"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    images   = models.ImageField(upload_to=images_live_upload_path)
    lives    = models.FileField(upload_to=videos_live_upload_path)
    comments = GenericRelation('CommentModel')
    publish  = models.BooleanField(default=True)
    tags     = models.ManyToManyField(TagModel, blank=True)
    like     = models.ManyToManyField(User, related_name='live_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    objects  = LiveManager()

    def __str__(self):
        return self.title

    def score(self):
        return self.read + self.like.count()*10 + self.read*self.like.count()/self.read*20

    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.filter(parent__isnull=True).count()

    def save(self, *args, **kwargs):
        if self.id is None:
            images = self.images
            lives = self.lives
            self.images = None
            self.lives = None
            super().save(*args, **kwargs)
            self.images = images
            self.lives = lives
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '02 Live'


class MusicQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) |
                Q(tags__tag__icontains=query) |
                Q(author__nickname__icontains=query) |
                Q(content__icontains=query) |
                Q(lyrics__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class MusicManager(models.Manager):
    def get_queryset(self):
        return MusicQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

def musics_upload_path(instance, filename):
    return f'musics/user_{instance.author.id}/object_{instance.id}/{filename}'

class MusicModel(models.Model):
    """MusicModel"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    lyrics   = models.TextField(blank=True, null=True)
    musics   = models.FileField(upload_to=musics_upload_path)
    comments = GenericRelation('CommentModel')
    publish  = models.BooleanField(default=True)
    download = models.BooleanField(default=True)
    tags     = models.ManyToManyField(TagModel, blank=True)
    like     = models.ManyToManyField(User, related_name='music_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    objects  = MusicManager()

    def __str__(self):
        return self.title

    def score(self):
        return self.read + self.like.count()*10 + self.read*self.like.count()/self.read*20

    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.filter(parent__isnull=True).count()

    def save(self, *args, **kwargs):
        if self.id is None:
            musics = self.musics
            self.musics = None
            super().save(*args, **kwargs)
            self.musics = musics
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '03 Music'

class PictureQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) |
                Q(tags__tag__icontains=query) |
                Q(author__nickname__icontains=query) |
                Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class PictureManager(models.Manager):
    def get_queryset(self):
        return PictureQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

def images_picture_upload_path(instance, filename):
    return f'images/images_picture/user_{instance.author.id}/object_{instance.id}/{filename}'

class PictureModel(models.Model):
    """PictureModel"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    images   = models.ImageField(upload_to=images_picture_upload_path)
    comments = GenericRelation('CommentModel')
    publish  = models.BooleanField(default=True)
    tags     = models.ManyToManyField(TagModel, blank=True)
    like     = models.ManyToManyField(User, related_name='picture_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    objects  = PictureManager()

    def __str__(self):
        return self.title

    def score(self):
        return self.read + self.like.count()*10 + self.read*self.like.count()/self.read*20

    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.filter(parent__isnull=True).count()

    def save(self, *args, **kwargs):
        if self.id is None:
            images = self.images
            self.images = None
            super().save(*args, **kwargs)
            self.images = images
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '04 Picture'


class BlogQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) |
                Q(tags__tag__icontains=query) |
                Q(author__nickname__icontains=query) |
                Q(content__icontains=query) |
                Q(richtext__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class BlogManager(models.Manager):
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

def images_blog_upload_path(instance, filename):
    return f'images/images_blog/user_{instance.author.id}/object_{instance.id}/{filename}'

class BlogModel(models.Model):
    """BlogModel"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    images   = models.ImageField(upload_to=images_blog_upload_path)
    richtext = RichTextUploadingField(blank=True, null=True)
    comments = GenericRelation('CommentModel')
    publish  = models.BooleanField(default=True)
    tags     = models.ManyToManyField(TagModel, blank=True)
    like     = models.ManyToManyField(User, related_name='blog_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    objects  = BlogManager()

    def __str__(self):
        return self.title

    def score(self):
        return self.read + self.like.count()*10 + self.read*self.like.count()/self.read*20

    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.filter(parent__isnull=True).count()

    def save(self, *args, **kwargs):
        if self.id is None:
            images = self.images
            self.images = None
            super().save(*args, **kwargs)
            self.images = images
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '05 Blog'


class ChatQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) |
                Q(tags__tag__icontains=query) |
                Q(author__nickname__icontains=query) |
                Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class ChatManager(models.Manager):
    def get_queryset(self):
        return ChatQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class ChatModel(models.Model):
    """ChatModel"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    comments = GenericRelation('CommentModel')
    publish  = models.BooleanField(default=True)
    tags     = models.ManyToManyField(TagModel, blank=True)
    like     = models.ManyToManyField(User, related_name='chat_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    joined   = models.IntegerField(blank=True, null=True, default=0)
    period   = models.DateField()
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    objects  = ChatManager()

    def __str__(self):
        return self.title

    def score(self):
        return self.read + self.like.count()*10 + self.read*self.like.count()/self.read*20

    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.filter(parent__isnull=True).count()

    def user_count(self):
        self.joined = self.comments.order_by('author').distinct().values_list('author').count()
        return self.joined

    class Meta:
        verbose_name_plural = '06 Chat'


class CollaboModel(models.Model):
    """CollaboModel"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    comments = GenericRelation('CommentModel')
    publish  = models.BooleanField(default=True)
    tags     = models.ManyToManyField(TagModel, blank=True)
    like     = models.ManyToManyField(User, related_name='collabo_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    period   = models.DateField()
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.filter(parent__isnull=True).count()

    class Meta:
        verbose_name_plural = '07 Collabo'


class TodoModel(models.Model):
    """TodoModel"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    priority_choice = (('danger', '高'), ('success', '普通'), ('info', '低'))
    priority = models.CharField(max_length=10, choices=priority_choice, default='success')
    duedate  = models.DateField()
    progress_choice = (('0', '未着手'), ('1', '進行中'), ('2', '完了'))
    progress = models.CharField(max_length=10, choices=progress_choice, default='0')
    comments = GenericRelation('CommentModel')
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.filter(parent__isnull=True).count()

    class Meta:
        verbose_name_plural = '08 ToDo'


class FollowModel(models.Model):
    """FollowModel"""
    follower  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.follower, self.following)

    class Meta:
        verbose_name_plural = '11 フォロー'


class NotificationModel(models.Model):
    """NotificationModel"""
    # {'1':'video', '2':'live', '3':'music', '4':'picture', '5':'blog', '6':'chat',
    # '7':'collabo', '8':'follow', '9':'like', '10':'reply', '11':'views'}
    user_from      = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE)
    user_to        = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, blank=True, null=True)
    type_no        = models.IntegerField(default=0)
    type_name      = models.CharField(max_length=7, blank=True, null=True)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    confirmed      = models.ManyToManyField(User, related_name='confirmed', blank=True)
    deleted        = models.ManyToManyField(User, related_name='deleted', blank=True)
    created        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content_object)

    class Meta:
        verbose_name_plural = '12 通知確認'


def images_adver_upload_path(instance, filename):
    return f'images/images_adver/user_{instance.author.id}/object_{instance.id}/{filename}'

def videos_adver_upload_path(instance, filename):
    return f'videos/videos_adver/user_{instance.author.id}/object_{instance.id}/{filename}'

class AdvertiseModel(models.Model):
    """AdvertiseModel"""
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=100)
    url     = models.URLField()
    content = models.TextField()
    images  = models.ImageField(upload_to=images_adver_upload_path)
    videos  = models.FileField(upload_to=videos_adver_upload_path)
    publish = models.BooleanField(default=True)
    read    = models.IntegerField(blank=True, null=True, default=0)
    choice  = (('0', '全体'), ('1', '個別'))
    type    = models.CharField(choices=choice, max_length=2, default='1')
    period  = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id is None:
            images = self.images
            videos = self.videos
            self.images = None
            self.videos = None
            super().save(*args, **kwargs)
            self.images = images
            self.videos = videos
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '13 広告設定'


class CommentModel(models.Model):
    """CommentModel"""
    author         = models.ForeignKey(User, on_delete=models.CASCADE)
    parent         = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply', blank=True, null=True)
    text           = models.TextField()
    like           = models.ManyToManyField(User, related_name='comment_like', blank=True)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def total_like(self):
        return self.like.count()

    def replies_count(self):
        return CommentModel.objects.filter(parent=self).count()

    class Meta:
        verbose_name_plural = '14 コメント'


class ProductModel(models.Model):
    name              = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=100)
    description       = models.TextField(blank=True)

    def __str__(self):
        return self.name


class PriceModel(models.Model):
    product         = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price           = models.IntegerField(default=0)

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
