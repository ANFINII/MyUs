from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.utils import timezone
from django_ulid.models import ulid
from api.models.master import Plan
from api.utils.enum.index import GenderType
from api.utils.functions.file import user_image


class UserManager(BaseUserManager):
    def create_user(self, email, username, nickname, password=None):
        if not email:
            raise ValueError("Users must have an email")
        elif not username:
            raise ValueError("Users must have an username")
        elif not nickname:
            raise ValueError("Users must have an nickname")
        user = self.model(email=self.normalize_email(email), username=username, nickname=nickname)
        user.set_password(password)
        user.is_active=False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, nickname, password):
        user = self.create_user(email, username, nickname, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User"""
    img         = "../static/img/user_icon.png"
    id          = models.BigAutoField(primary_key=True)
    ulid        = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    username    = models.CharField(max_length=20, unique=True)
    nickname    = models.CharField(max_length=80, unique=True)
    email       = models.EmailField(max_length=255, unique=True)
    avatar      = models.ImageField(upload_to=user_image, default=img, blank=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    last_login  = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(default=timezone.now())

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "nickname"]

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def full_name(self):
        return self.profile.last_name + " " + self.profile.first_name
    full_name.short_description = "name"

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

    def street(self):
        return self.profile.street

    def image(self):
        if self.avatar:
            return self.avatar.url

    def banner(self):
        if self.mypage.banner:
            return self.mypage.banner.url

    def plan(self):
        return self.user_plan.plan.name

    def plan_start_date(self):
        return self.user_plan.start_date

    def plan_end_date(self):
        return self.user_plan.end_date

    def save(self, *args, **kwargs):
        if self.id is None:
            avatar = self.avatar
            self.avatar = None
            super().save(*args, **kwargs)
            self.avatar = avatar
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "user"
        verbose_name_plural = "001 User"
        indexes = [
            models.Index(fields=["email"], name="email_idx"),
            models.Index(fields=["username"], name="username_idx"),
            models.Index(fields=["nickname"], name="nickname_idx"),
        ]


class ProfileManager(models.Manager):
    def get_queryset(self):
        return super(ProfileManager,self).get_queryset().select_related("user")

class Profile(models.Model):
    """Profile"""
    id           = models.BigAutoField(primary_key=True)
    gender_type  = ((GenderType.MALE, "男性"), (GenderType.FEMALE, "女性"), (GenderType.SECRET, "秘密"))
    message      = "電話番号は090-1234-5678の形式で入力する必要があります。最大15桁まで入力できます"
    phone_no     = RegexValidator(regex=r"\d{2,4}-?\d{2,4}-?\d{3,4}", message=message)
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name    = models.CharField(max_length=50)
    first_name   = models.CharField(max_length=50)
    birthday     = models.DateField(blank=True, null=True)
    gender       = models.CharField(choices=gender_type, max_length=6)
    phone        = models.CharField(validators=[phone_no], max_length=15, blank=True)
    country_code = models.CharField(max_length=255, default="JP")
    postal_code  = models.CharField(max_length=255, blank=True)
    prefecture   = models.CharField(max_length=255, blank=True)
    city         = models.CharField(max_length=255, blank=True)
    street       = models.CharField(max_length=255, blank=True)
    introduction = models.TextField(blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.nickname

    class Meta:
        db_table = "user_profile"
        verbose_name_plural = "001 profile"

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """ユーザー作成時に空のProfileも作成する"""
    if kwargs["created"]:
        Profile.objects.get_or_create(user=kwargs["instance"])


class MyPageManager(models.Manager):
    def get_queryset(self):
        return super(MyPageManager,self).get_queryset().select_related("user")

class MyPage(models.Model):
    """MyPage"""
    img             = "../static/img/MyUs_banner.png"
    id              = models.BigAutoField(primary_key=True)
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    banner          = models.ImageField(upload_to=user_image, default=img, blank=True)
    email           = models.EmailField(max_length=255, blank=True)
    content         = models.TextField(blank=True)
    follower_count  = models.IntegerField(verbose_name="follower", default=0)
    following_count = models.IntegerField(verbose_name="follow", default=0)
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
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "user_mypage"
        verbose_name_plural = "001 MyPage"

@receiver(post_save, sender=User)
def create_mypage(sender, **kwargs):
    """ユーザー作成時に空のMyPageも作成する"""
    if kwargs["created"]:
        MyPage.objects.get_or_create(user=kwargs["instance"])


class UserNotification(models.Model):
    """UserNotification"""
    id         = models.BigAutoField(primary_key=True)
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    is_video   = models.BooleanField(default=False)
    is_music   = models.BooleanField(default=False)
    is_comic   = models.BooleanField(default=False)
    is_picture = models.BooleanField(default=False)
    is_blog    = models.BooleanField(default=False)
    is_chat    = models.BooleanField(default=False)
    is_follow  = models.BooleanField(default=True)
    is_reply   = models.BooleanField(default=True)
    is_like    = models.BooleanField(default=True)
    is_views   = models.BooleanField(default=True)

    def __str__(self):
        return self.user.nickname

    class Meta:
        db_table = 'user_notification'
        verbose_name_plural = '001 通知設定'

@receiver(post_save, sender=User)
def create_user_notification(sender, **kwargs):
    """ユーザー作成時に空のuser_notificationも作成する"""
    if kwargs['created']:
        UserNotification.objects.get_or_create(user=kwargs['instance'])


class UserPlan(models.Model):
    """UserPlan"""
    id           = models.BigAutoField(primary_key=True)
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_plan')
    plan         = models.ForeignKey(Plan, on_delete=models.CASCADE, default=1)
    customer_id  = models.CharField(max_length=255)
    subscription = models.CharField(max_length=255)
    is_paid      = models.BooleanField(default=False)
    start_date   = models.DateTimeField(blank=True, null=True)
    end_date     = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.plan.name

    class Meta:
        db_table = 'user_plan'
        verbose_name_plural = '001 UserPlan'

@receiver(post_save, sender=User)
def create_user_plan(sender, **kwargs):
    """ユーザー作成時に空のuser_planも作成する"""
    if kwargs['created']:
        UserPlan.objects.get_or_create(user=kwargs['instance'])
