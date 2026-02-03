from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from api.db.models.user import User


class SearchTag(models.Model):
    """SearchTag"""
    id       = models.BigAutoField(primary_key=True)
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    sequence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], default=20)
    name     = models.CharField(max_length=30)
    created  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "searchtag"
        verbose_name_plural = "08 検索タグ"


class Follow(models.Model):
    """Follow"""
    id        = models.BigAutoField(primary_key=True)
    follower  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    is_follow = models.BooleanField(default=True)
    created   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} : {self.following}"

    class Meta:
        db_table = "follow"
        verbose_name_plural = "10 フォロー"
        indexes = [
            models.Index(fields=["follower"], name="follower_idx"),
            models.Index(fields=["following"], name="following_idx"),
            models.Index(fields=["follower", "following"], name="follower_following_idx"),
        ]
