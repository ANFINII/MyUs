from django.db import models


class Plan(models.Model):
    """Plan"""
    id            = models.BigAutoField(primary_key=True)
    name          = models.CharField(max_length=30)
    stripe_api_id = models.CharField(max_length=30)
    price         = models.IntegerField(default=0)
    max_advertise = models.IntegerField(default=0)
    description   = models.TextField(blank=True)

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
    id      = models.BigAutoField(primary_key=True)
    jp_name = models.CharField(max_length=30)
    en_name = models.CharField(max_length=60)

    def __str__(self):
        return self.jp_name

    class Meta:
        db_table = "hashtag"
        verbose_name_plural = "001 ハッシュタグ"
