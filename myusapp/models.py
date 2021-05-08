from django.db import models
from django.db.models.fields import BooleanField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.core.mail import send_mail
from ckeditor_uploader.fields import RichTextUploadingField
# from ckeditor.fields import RichTextField

# Create your models here.

class UserManager(BaseUserManager):
    """ユーザーマネージャー"""
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')
        elif not email:
            raise ValueError('Users must have an email address')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(username, email=self.normalize_email(email), password=password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル"""
    user_image      = models.ImageField(upload_to='users/', default='../static/img/user_icon.png', blank=True, null=True)
    email           = models.EmailField(max_length=120, unique=True)
    username        = models.CharField(max_length=30, unique=True)
    nickname        = models.CharField(max_length=60, unique=True)
    full_name       = models.CharField(max_length=60, blank=True)
    last_name       = models.CharField(max_length=30, blank=True)
    first_name      = models.CharField(max_length=30, blank=True)
    
    birthday        = models.DateField(blank=True, null=True)
    year            = models.IntegerField(blank=True, null=True)
    month           = models.IntegerField(blank=True, null=True)
    day             = models.IntegerField(blank=True, null=True)
    age             = models.IntegerField(blank=True, null=True)
    
    GENDER_CHOICES  = (('0', '男性'), ('1', '女性'), ('2', '秘密'))
    gender          = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True)
    
    phone_no        = RegexValidator(regex=r'\d{2,4}-?\d{2,4}-?\d{3,4}', message = ('電話番号は090-1234-5678の形式で入力する必要があります。最大15桁まで入力できます。'))
    phone           = models.CharField(validators=[phone_no], max_length=15, blank=True, default='000-0000-0000')
    
    location        = models.CharField(max_length=255, blank=True)
    profession      = models.CharField(max_length=120, blank=True)
    introduction    = models.TextField(blank=True)
    
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    last_login      = models.DateTimeField(_('last login'), auto_now_add=True)
    date_joined     = models.DateTimeField(_('date joined'), default=timezone.now)
    
    # Myページ用フィールド
    mypage_image    = models.ImageField(upload_to='users/', default='../static/img/MyUs_banner.png', blank=True, null=True)
    mypage_email    = models.EmailField(max_length=120, blank=True, null=True, default='abc@gmail.com')
    content         = models.TextField(blank=True)
    follower_count  = models.IntegerField(verbose_name='follower', blank=True, null=True, default=0)
    following_count = models.IntegerField(verbose_name='follow', blank=True, null=True, default=0)
    
    objects = UserManager()
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['username', 'email']
    
    class Meta:
        verbose_name_plural = '00 User'
    
    def has_perm(self, perm, obj=None):
        "ユーザーにパーミッション権限を持ちますか？"
        return True
    
    def has_module_perms(self, app_label):
        "ユーザーにパーミッションのリストを表示させますか?"
        return True
    
    def get_username(self):
        """nickname"""
        return self.nickname
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
        
    def get_following_count(self):
        self.following_count = FollowModel.objects.filter(follower=User.id).count()
        return self.following_count
    
    def get_follower_count(self):
        self.follower_count = FollowModel.objects.filter(following=User.id).count()
        return self.follower_count

@property
def image_url(self):
    if self.user_image and hasattr(self.user_image, 'url'):
        return self.user_image.url
    
@property
def mypage_image(self):
    if self.mypage_image and hasattr(self.mypage_image, 'url'):
        return self.mypage_image.url
    
class FollowModel(models.Model):
    """ここにメソッドの説明を記述する"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name='follow')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} : {}".format(self.follower.username, self.following.username)
        
    class Meta:
        verbose_name_plural = '09 フォロー'
        
class SearchTag(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    sequence = models.IntegerField(validators=[MaxValueValidator(10)], default=1)
    searchtag = models.CharField(max_length=12, null=True)

    def __str__(self):
        return self.searchtag
    
    class Meta:
        verbose_name_plural = '10 検索タグ'

class Tag(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=12, null=True)

    def __str__(self):
        return self.tag
    
    class Meta:
        verbose_name_plural = '11 ハッシュタグ'

class VideoModel(models.Model):
    """ここにメソッドの説明を記述する"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    images   = models.ImageField(upload_to='images/')
    videos   = models.FileField(upload_to='videos/')
    comments = GenericRelation('Comment')
    publish  = BooleanField(default=True)
    tags     = models.ManyToManyField(Tag, blank=True)
    like     = models.ManyToManyField(User, related_name='video_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.all().count()

    class Meta:
        verbose_name_plural = '01 Video'

class LiveModel(models.Model):
    """ここにメソッドの説明を記述する"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    images   = models.ImageField(upload_to='images/')
    lives    = models.FileField(upload_to='lives/')
    comments = GenericRelation('Comment')
    publish  = BooleanField(default=True)
    tags     = models.ManyToManyField(Tag, blank=True)
    like     = models.ManyToManyField(User, related_name='live_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.all().count()

    class Meta:
        verbose_name_plural = '02 Live'

class MusicModel(models.Model):
    """ここにメソッドの説明を記述する"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    lyrics   = models.TextField(blank=True, null=True)
    musics   = models.FileField(upload_to='musics/')
    comments = GenericRelation('Comment')
    publish  = BooleanField(default=True)
    tags     = models.ManyToManyField(Tag, blank=True)
    like     = models.ManyToManyField(User, related_name='music_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.all().count()

    class Meta:
        verbose_name_plural = '03 Music'

class PictureModel(models.Model):
    """ここにメソッドの説明を記述する"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    images   = models.ImageField(upload_to='images/')
    comments = GenericRelation('Comment')
    publish  = BooleanField(default=True)
    tags     = models.ManyToManyField(Tag, blank=True)
    like     = models.ManyToManyField(User, related_name='picture_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.all().count()

    class Meta:
        verbose_name_plural = '04 Picture'

class BlogModel(models.Model):
    """ここにメソッドの説明を記述する"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    images   = models.ImageField(upload_to='images/')
    richtext = RichTextUploadingField(blank=True, null=True)
    comments = GenericRelation('Comment')
    publish  = BooleanField(default=True)
    tags     = models.ManyToManyField(Tag, blank=True)
    like     = models.ManyToManyField(User, related_name='blog_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.all().count()
    
    class Meta:
        verbose_name_plural = '05 Blog'
    
class ChatModel(models.Model):
    """ここにメソッドの説明を記述する"""
    author    = models.ForeignKey(User, on_delete=models.CASCADE)
    title     = models.CharField(max_length=100)
    content   = models.TextField()
    comments  = GenericRelation('Comment')
    publish   = BooleanField(default=True)
    tags      = models.ManyToManyField(Tag, blank=True)
    like      = models.ManyToManyField(User, related_name='chat_like', blank=True)
    read      = models.IntegerField(blank=True, null=True, default=0)
    usercount = models.IntegerField(blank=True, null=True, default=0)
    created   = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.all().count()

    def user_count(self):
        self.usercount = self.comments.order_by('author').distinct().values_list('author').count()
        return self.usercount
        
    class Meta:
        verbose_name_plural = '06 Chat'  

class CollaboModel(models.Model):
    """ここにメソッドの説明を記述する"""
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    comments = GenericRelation('Comment')
    publish  = BooleanField(default=True)
    tags     = models.ManyToManyField(Tag, blank=True)
    like     = models.ManyToManyField(User, related_name='collabo_like', blank=True)
    read     = models.IntegerField(blank=True, null=True, default=0)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def total_like(self):
        return self.like.count()

    def comment_count(self):
        return self.comments.all().count()

    class Meta:
        verbose_name_plural = '07 Collabo'

PRIORITY = (('danger','高'),('success','普通'),('info','低'))
class TodoModel(models.Model):
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY)
    duedate  = models.DateField()
    comments = GenericRelation('Comment')
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('todo_detail', kwargs={'pk':self.pk})

    def comment_count(self):
        return self.comments.all().count()

    class Meta:
        verbose_name_plural = '08 ToDo'

class Comment(models.Model):
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
    
    class Meta:
        verbose_name_plural = '12 コメント'