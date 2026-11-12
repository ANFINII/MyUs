from django.db import models
from django_ulid.models import ulid


class Category(models.Model):
    """Category"""
    id      = models.BigAutoField(primary_key=True)
    ulid    = models.CharField(max_length=26, unique=True, editable=False, default=ulid.new)
    jp_name = models.CharField(max_length=120)
    en_name = models.CharField(max_length=120)

    def __str__(self):
        return self.jp_name

    class Meta:
        db_table = "category"
        verbose_name_plural = "001 カテゴリー"


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
