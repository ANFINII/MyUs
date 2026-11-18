from django.db import models
from myus.utils.functions.common import new_ulid
from .media import Music
from .user import User


class Playlist(models.Model):
    """Playlist"""
    id          = models.BigAutoField(primary_key=True)
    ulid        = models.CharField(max_length=26, unique=True, editable=False, default=new_ulid)
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    title       = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    image       = models.ImageField(max_length=255, blank=True)
    publish     = models.BooleanField(default=False)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "playlist"
        verbose_name_plural = "02 Playlist"
        indexes = [models.Index(fields=["author", "-updated"], name="playlist_author_updated_idx")]


class PlaylistMusic(models.Model):
    """PlaylistMusic"""
    id       = models.BigAutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="playlist_musics")
    music    = models.ForeignKey(Music, on_delete=models.CASCADE)
    sequence = models.IntegerField()

    class Meta:
        db_table = "playlist_music"
        verbose_name_plural = "02 PlaylistMusic"
        constraints = [models.UniqueConstraint(fields=["playlist", "music"], name="playlist_music_uniq")]
        indexes = [models.Index(fields=["playlist", "sequence"], name="playlist_music_seq_idx")]
