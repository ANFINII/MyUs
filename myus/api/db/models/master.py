from django.db import models
from django_ulid.models import ulid


class Plan(models.Model):
    """Plan"""
    id            = models.BigAutoField(primary_key=True)
    name          = models.CharField(max_length=30)
    stripe_api_id = models.CharField(max_length=30)
    price         = models.IntegerField()
    max_advertise = models.IntegerField()
    description   = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "plan"
        verbose_name_plural = "001 Plan"
        indexes = [models.Index(fields=["stripe_api_id"], name="stripe_api_idx")]


class Category(models.Model):
    """Category"""
    id      = models.BigAutoField(primary_key=True)
    jp_name = models.CharField(max_length=120)
    en_name = models.CharField(max_length=120)

    def __str__(self):
        return self.jp_name

    class Meta:
        db_table = "category"
        verbose_name_plural = "001 カテゴリー"


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


class NgWord(models.Model):
    """NgWord"""
    id      = models.BigAutoField(primary_key=True)
    word    = models.CharField(max_length=30, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word

    class Meta:
        db_table = "ng_word"
        verbose_name_plural = "001 NGワード"
