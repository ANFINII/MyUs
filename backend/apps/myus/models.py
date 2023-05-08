from datetime import date
from django.db import models
from django.db.models import Q, Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.mail import send_mail
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.utils import timezone
from django_quill.fields import QuillField


class UserManager(BaseUserManager):
    """UserManager"""
    def create_user(self, email, username, nickname, password=None):
        if not email:
            raise ValueError('Users must have an email')
        elif not username:
            raise ValueError('Users must have an username')
        elif not nickname:
            raise ValueError('Users must have an nickname')
        user = self.model(email=self.normalize_email(email), username=username, nickname=nickname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, nickname, password):
        user = self.create_user(email, username, nickname, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return super(UserManager,self).get_queryset().select_related('mypage')

def user_icon(instance, filename):
    return f'users/images_user/user_{instance.id}/{filename}'

class User(AbstractBaseUser, PermissionsMixin):
    """User"""
    img         = '../static/img/user_icon.png'
    avatar      = models.ImageField(upload_to=user_icon, default=img, blank=True, null=True)
    email       = models.EmailField(max_length=255, unique=True)
    username    = models.CharField(max_length=20, unique=True)
    nickname    = models.CharField(max_length=80, unique=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    last_login  = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nickname']

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def fullname(self):
        return self.profile.last_name + ' ' + self.profile.first_name
    fullname.short_description = 'name'

    def year(self):
        if self.birthday:
            return self.profile.birthday.year

    def month(self):
        if self.birthday:
            return self.profile.birthday.month

    def day(self):
        if self.birthday:
            return self.profile.birthday.day

    def age(self):
        if self.profile:
            birthday = self.profile.birthday
            DAYS_IN_YEAR = 365.2425
            return int((date.today() - birthday).days / DAYS_IN_YEAR)

    def gender(self):
        return self.profile.gender

    def birthday(self):
        return self.profile.birthday

    def prefecture(self):
        return self.profile.prefecture

    def city(self):
        return self.profile.city

    def address(self):
        return self.profile.address

    def building(self):
        return self.profile.building

    def image(self):
        if self.avatar:
            return self.avatar.url

    def banner(self):
        if self.mypage.banner:
            return self.mypage.banner.url

    def plan(self):
        plan_dict = {'free': 'Free', 'basic': 'Basic', 'standard': 'Standard', 'premium': 'Premium'}
        return [value for key, value in plan_dict.items() if self.mypage.plan in key]

    def save(self, *args, **kwargs):
        if self.id is None:
            avatar = self.avatar
            self.avatar = None
            super().save(*args, **kwargs)
            self.avatar = avatar
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'user'
        verbose_name_plural = '001 User'
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['username'], name='username_idx'),
            models.Index(fields=['nickname'], name='nickname_idx'),
        ]


class ProfileManager(models.Manager):
    def get_queryset(self):
        return super(ProfileManager,self).get_queryset().select_related('user')

class Profile(models.Model):
    gender_type  = (('0', '男性'), ('1', '女性'), ('2', '秘密'))
    message      = '電話番号は090-1234-5678の形式で入力する必要があります。最大15桁まで入力できます'
    phone_no     = RegexValidator(regex=r'\d{2,4}-?\d{2,4}-?\d{3,4}', message=message)
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name    = models.CharField(max_length=50)
    first_name   = models.CharField(max_length=50)
    birthday     = models.DateField(blank=True, null=True)
    gender       = models.CharField(choices=gender_type, max_length=1)
    phone        = models.CharField(validators=[phone_no], max_length=15, blank=True)
    country_code = models.CharField(max_length=255, default='JP')
    postal_code  = models.CharField(max_length=255, blank=True)
    prefecture   = models.CharField(max_length=255, blank=True)
    city         = models.CharField(max_length=255, blank=True)
    address      = models.CharField(max_length=255, blank=True)
    building     = models.CharField(max_length=255, blank=True)
    introduction = models.TextField(blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.nickname

    class Meta:
        db_table = 'profile'
        verbose_name_plural = '001 profile'

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """ユーザー作成時に空のProfileも作成する"""
    if kwargs['created']:
        Profile.objects.get_or_create(user=kwargs['instance'])


class MyPageManager(models.Manager):
    def get_queryset(self):
        return super(MyPageManager,self).get_queryset().select_related('user')

def mypage_banner(instance, filename):
    return f'users/images_mypage/user_{instance.id}/{filename}'

class MyPage(models.Model):
    img             = '../static/img/MyUs_banner.png'
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    banner          = models.ImageField(upload_to=mypage_banner, default=img, blank=True, null=True)
    email           = models.EmailField(max_length=255, blank=True)
    content         = models.TextField(blank=True)
    follower_count  = models.IntegerField(verbose_name='follower', default=0)
    following_count = models.IntegerField(verbose_name='follow', default=0)
    tag_manager_id  = models.CharField(max_length=10, blank=True)
    is_advertise    = models.BooleanField(default=True)

    objects = MyPageManager()

    def __str__(self):
        return self.user.nickname

    def save(self, *args, **kwargs):
        if self.id is None:
            banner = self.banner
            self.banner = None
            super().save(*args, **kwargs)
            self.banner = banner
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'mypage'
        verbose_name_plural = '001 MyPage'

@receiver(post_save, sender=User)
def create_mypage(sender, **kwargs):
    """ユーザー作成時に空のMyPageも作成する"""
    if kwargs['created']:
        MyPage.objects.get_or_create(user=kwargs['instance'])


class NotificationSetting(models.Model):
    """NotificationSetting"""
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    is_video   = models.BooleanField(default=False)
    is_music   = models.BooleanField(default=False)
    is_picture = models.BooleanField(default=False)
    is_blog    = models.BooleanField(default=False)
    is_chat    = models.BooleanField(default=False)
    is_collabo = models.BooleanField(default=False)
    is_follow  = models.BooleanField(default=True)
    is_reply   = models.BooleanField(default=True)
    is_like    = models.BooleanField(default=True)
    is_views   = models.BooleanField(default=True)

    def __str__(self):
        return self.user.nickname

    class Meta:
        db_table = 'notification_setting'
        verbose_name_plural = '001 通知設定'

@receiver(post_save, sender=User)
def create_notification_setting(sender, **kwargs):
    """ユーザー作成時に空のnotification_settingも作成する"""
    if kwargs['created']:
        NotificationSetting.objects.get_or_create(user=kwargs['instance'])


class PlanMaster(models.Model):
    name          = models.CharField(max_length=30)
    stripe_api_id = models.CharField(max_length=30)
    price         = models.IntegerField(default=0)
    max_advertise = models.IntegerField(default=0)
    description   = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plan_master'
        verbose_name_plural = '001 PlanMaster'
        indexes = [models.Index(fields=['stripe_api_id'], name='stripe_api_idx')]


class UserPlan(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    plan       = models.ForeignKey(PlanMaster, on_delete=models.CASCADE, default=1)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date   = models.DateTimeField(blank=True, null=True)
    is_free    = models.BooleanField(default=True)

    def __str__(self):
        return self.plan.name

    class Meta:
        db_table = 'user_plan'
        verbose_name_plural = '001 UserPlan'

@receiver(post_save, sender=User)
def create_user_plan(sender, **kwargs):
    """ユーザー作成時に空のMyPageも作成する"""
    if kwargs['created']:
        UserPlan.objects.get_or_create(user=kwargs['instance'])


class AccessLog(models.Model):
    ip_address = models.GenericIPAddressField()
    type       = models.CharField(max_length=7, blank=True)
    type_id    = models.BigIntegerField(blank=True, null=True)
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ip_address)

    class Meta:
        db_table = 'access_log'
        verbose_name_plural = '002 Access Log'
        indexes = [
            models.Index(fields=['ip_address', 'type', 'type_id'], name='ip_address_type_idx'),
        ]


class SearchTag(models.Model):
    """SearchTag"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    sequence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], default=20)
    name     = models.CharField(max_length=30)
    created  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'searchtag'
        verbose_name_plural = '08 検索タグ'


class HashTag(models.Model):
    """HashTag"""
    jp_name = models.CharField(max_length=30)
    en_name = models.CharField(max_length=60)

    def __str__(self):
        return self.jp_name

    class Meta:
        db_table = 'hashtag'
        verbose_name_plural = '09 ハッシュタグ'


class MediaModel:
    def __str__(self):
        return self.title

    def total_like(self):
        return self.like.count()
    total_like.short_description = 'like'

    def comment_count(self):
        return self.comment.count()
    comment_count.short_description = 'comment'

    def score(self):
        return int(self.read + self.like.count()*10 + self.read*self.like.count()/(self.read+1)*20)

class MediaManager:
    def search(self, query=None):
        return self.get_queryset().search(query=query)


class VideoQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query:
            or_lookup = (
                Q(title__icontains=query) |
                Q(hashtag__jp_name__icontains=query) |
                Q(author__nickname__icontains=query) |
                Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class VideoManager(models.Manager, MediaManager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db).select_related('author').prefetch_related('like', 'comment')

def images_video_upload(instance, filename):
    return f'images/images_video/user_{instance.author_id}/object_{instance.id}/{filename}'

def videos_video_upload(instance, filename):
    return f'videos/videos_video/user_{instance.author_id}/object_{instance.id}/{filename}'

class Video(models.Model, MediaModel):
    """Video"""
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=100)
    content = models.TextField()
    image   = models.ImageField(upload_to=images_video_upload)
    video   = models.FileField(upload_to=videos_video_upload)
    convert = models.FileField(upload_to=videos_video_upload)
    comment = GenericRelation('Comment')
    hashtag = models.ManyToManyField(HashTag, blank=True)
    like    = models.ManyToManyField(User, related_name='video_like', blank=True)
    read    = models.IntegerField(default=0)
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = VideoManager()

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
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'video'
        verbose_name_plural = '01 Video'


class MusicQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query:
            or_lookup = (
                Q(title__icontains=query) |
                Q(hashtag__jp_name__icontains=query) |
                Q(author__nickname__icontains=query) |
                Q(content__icontains=query) |
                Q(lyric__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class MusicManager(models.Manager, MediaManager):
    def get_queryset(self):
        return MusicQuerySet(self.model, using=self._db).select_related('author').prefetch_related('like', 'comment')

def musics_upload(instance, filename):
    return f'musics/user_{instance.author_id}/object_{instance.id}/{filename}'

class Music(models.Model, MediaModel):
    """Music"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    lyric    = models.TextField(blank=True)
    music    = models.FileField(upload_to=musics_upload)
    comment  = GenericRelation('Comment')
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name='music_like', blank=True)
    read     = models.IntegerField(default=0)
    download = models.BooleanField(default=True)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    objects = MusicManager()

    def save(self, *args, **kwargs):
        if self.id is None:
            music = self.music
            self.music = None
            super().save(*args, **kwargs)
            self.music = music
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'music'
        verbose_name_plural = '02 Music'


class PictureQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query:
            or_lookup = (
                Q(title__icontains=query) |
                Q(hashtag__jp_name__icontains=query) |
                Q(author__nickname__icontains=query) |
                Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class PictureManager(models.Manager, MediaManager):
    def get_queryset(self):
        return PictureQuerySet(self.model, using=self._db).select_related('author').prefetch_related('like', 'comment')

def images_picture_upload(instance, filename):
    return f'images/images_picture/user_{instance.author_id}/object_{instance.id}/{filename}'

class Picture(models.Model, MediaModel):
    """Picture"""
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=100)
    content = models.TextField()
    image   = models.ImageField(upload_to=images_picture_upload)
    comment = GenericRelation('Comment')
    hashtag = models.ManyToManyField(HashTag, blank=True)
    like    = models.ManyToManyField(User, related_name='picture_like', blank=True)
    read    = models.IntegerField(default=0)
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PictureManager()

    def save(self, *args, **kwargs):
        if self.id is None:
            image = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'picture'
        verbose_name_plural = '03 Picture'


class BlogQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query:
            or_lookup = (
                Q(title__icontains=query) |
                Q(hashtag__jp_name__icontains=query) |
                Q(author__nickname__icontains=query) |
                Q(content__icontains=query) |
                Q(richtext__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class BlogManager(models.Manager, MediaManager):
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db).select_related('author').prefetch_related('like', 'comment')

def images_blog_upload(instance, filename):
    return f'images/images_blog/user_{instance.author_id}/object_{instance.id}/{filename}'

class Blog(models.Model, MediaModel):
    """Blog"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    richtext = models.TextField()
    delta    = QuillField()
    image    = models.ImageField(upload_to=images_blog_upload)
    comment  = GenericRelation('Comment')
    hashtag  = models.ManyToManyField(HashTag, blank=True)
    like     = models.ManyToManyField(User, related_name='blog_like', blank=True)
    read     = models.IntegerField(default=0)
    publish  = models.BooleanField(default=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    objects = BlogManager()

    def save(self, *args, **kwargs):
        if self.id is None:
            image = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'blog'
        verbose_name_plural = '04 Blog'


class ChatQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query:
            or_lookup = (
                Q(title__icontains=query) |
                Q(hashtag__jp_name__icontains=query) |
                Q(author__nickname__icontains=query) |
                Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class ChatManager(models.Manager, MediaManager):
    def get_queryset(self):
        return ChatQuerySet(self.model, using=self._db).select_related('author').prefetch_related('like', 'message')

class Chat(models.Model):
    """Chat"""
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=100)
    content = models.TextField()
    hashtag = models.ManyToManyField(HashTag, blank=True)
    like    = models.ManyToManyField(User, related_name='chat_like', blank=True)
    read    = models.IntegerField(default=0)
    period  = models.DateField()
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ChatManager()

    def __str__(self):
        return self.title

    def total_like(self):
        return self.like.count()
    total_like.short_description = 'like'

    def thread_count(self):
        return self.message.filter(parent__isnull=True).count()
    thread_count.short_description = 'thread'

    def joined_count(self):
        return self.message.values_list('author').distinct().count()
    joined_count.short_description = 'joined'

    def score(self):
        return int(self.read + self.like.count()*10 + self.read*self.like.count()/(self.read+1)*20)

    class Meta:
        db_table = 'chat'
        verbose_name_plural = '05 Chat'


class Collabo(models.Model, MediaModel):
    """Collabo"""
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=100)
    content = models.TextField()
    comment = GenericRelation('Comment')
    hashtag = models.ManyToManyField(HashTag, blank=True)
    like    = models.ManyToManyField(User, related_name='collabo_like', blank=True)
    read    = models.IntegerField(default=0)
    period  = models.DateField()
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'collabo'
        verbose_name_plural = '06 Collabo'


class Todo(models.Model):
    """Todo"""
    priority_type = (('danger', '高'), ('success', '普通'), ('info', '低'))
    progress_type = (('0', '未着手'), ('1', '進行中'), ('2', '完了'))
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    priority = models.CharField(max_length=10, choices=priority_type)
    progress = models.CharField(max_length=10, choices=progress_type)
    comment  = GenericRelation('Comment')
    duedate  = models.DateField()
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comment.count()
    comment_count.short_description = 'comment'

    class Meta:
        db_table = 'todo'
        verbose_name_plural = '07 ToDo'


class Follow(models.Model):
    """Follow"""
    follower  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower} : {self.following}'

    class Meta:
        db_table = 'follow'
        verbose_name_plural = '10 フォロー'
        indexes = [
            models.Index(fields=['follower'], name='follower_idx'),
            models.Index(fields=['following'], name='following_idx'),
            models.Index(fields=['follower', 'following'], name='follower_following_idx'),
        ]


class Notification(models.Model):
    """Notification"""
    # 'video': 1, 'music': 2, 'picture': 3, 'blog': 4, 'chat': 5
    # 'collabo': 6, 'follow': 7, 'like': 8, 'reply': 9, 'views': 10
    user_from      = models.ForeignKey(User, related_name='user_from', on_delete=models.CASCADE)
    user_to        = models.ForeignKey(User, related_name='user_to', on_delete=models.CASCADE, blank=True, null=True)
    type_no        = models.IntegerField()
    type_name      = models.CharField(max_length=7, blank=True)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    confirmed      = models.ManyToManyField(User, related_name='confirmed', blank=True)
    deleted        = models.ManyToManyField(User, related_name='deleted', blank=True)
    created        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content_object)

    def title(self):
        return self.content_object
    title.short_description = 'title'

    def confirmed_count(self):
        return self.confirmed.count()
    confirmed_count.short_description = 'confirmed'

    def deleted_count(self):
        return self.deleted.count()
    deleted_count.short_description = 'deleted'

    class Meta:
        db_table = 'notification'
        verbose_name_plural = '11 通知確認'
        indexes = [
            models.Index(fields=['user_from', 'user_to'], name='notification_from_to_idx'),
            models.Index(fields=['type_no', 'object_id'], name='notification_type_object_idx'),
        ]


def images_adver_upload(instance, filename):
    return f'images/images_adver/user_{instance.author_id}/object_{instance.id}/{filename}'

def videos_adver_upload(instance, filename):
    return f'videos/videos_adver/user_{instance.author_id}/object_{instance.id}/{filename}'

class Advertise(models.Model):
    """Advertise"""
    choice  = (('all', '全体'), ('one', '個別'))
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=100)
    url     = models.URLField()
    content = models.TextField()
    image   = models.ImageField(upload_to=images_adver_upload)
    video   = models.FileField(upload_to=videos_adver_upload)
    read    = models.IntegerField(default=0)
    type    = models.CharField(choices=choice, max_length=3)
    period  = models.DateField()
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id is None:
            image = self.image
            video  = self.video
            self.image = None
            self.video  = None
            super().save(*args, **kwargs)
            self.image = image
            self.video  = video
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'advertise'
        verbose_name_plural = '12 広告設定'


class CommentManager(models.Manager):
    def get_queryset(self):
        qs = super(CommentManager,self).get_queryset().annotate(reply_count=Count('reply'))
        return qs.select_related('author', 'parent').prefetch_related('like')

class Comment(models.Model):
    """Comment"""
    author         = models.ForeignKey(User, on_delete=models.CASCADE)
    parent         = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply', blank=True, null=True)
    text           = models.TextField()
    like           = models.ManyToManyField(User, related_name='comment_like', blank=True)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    def __str__(self):
        return str(self.id)

    def total_like(self):
        return self.like.count()
    total_like.short_description = 'like'

    def reply_count(self):
        return self.reply.filter(parent=self).count()
    reply_count.short_description = 'reply'

    class Meta:
        db_table = 'comment'
        verbose_name_plural = '13 コメント'
        indexes = [
            models.Index(fields=['parent'], name='comment_parent_idx'),
        ]


class MessageManager(models.Manager):
    def get_queryset(self):
        qs = super(MessageManager,self).get_queryset().annotate(reply_count=Count('reply'))
        return qs.select_related('author', 'parent', 'chat')

class Message(models.Model):
    """Message"""
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    chat    = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='message')
    parent  = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply', blank=True, null=True)
    text    = models.TextField()
    delta   = QuillField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = MessageManager()

    def __str__(self):
        return str(self.id)

    def reply_count(self):
       return self.reply.filter(parent=self).count()
    reply_count.short_description = 'reply'

    class Meta:
        db_table = 'message'
        verbose_name_plural = '14 メッセージ'
        indexes = [
            models.Index(fields=['parent'], name='message_parent_idx'),
        ]


class Product(models.Model):
    name              = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=100)
    description       = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'


class Price(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price           = models.IntegerField()

    def __str__(self):
        return self.stripe_price_id

    def get_display_price(self):
        return '{0:.2f}'.format(self.price / 100)

    class Meta:
        db_table = 'price'
