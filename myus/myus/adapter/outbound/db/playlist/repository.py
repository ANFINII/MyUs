from django.db import transaction
from django.db.models import Prefetch, Q
from django.db.models.query import QuerySet
from myus.db.models.playlist import Playlist, PlaylistAudio
from myus.domain.playlist.data import PlaylistData
from myus.domain.playlist.interface import FilterOption, PageOption, PlaylistInterface, SortOption
from myus.domain.playlist.validation import validate
from myus.utils.common.result import FatalError, Result
from ._convert import convert_data, marshal_data
from ..common import get_save_new_ids, page_queryset, sort_ids


PLAYLIST_FIELDS = ["author_id", "title", "description", "image", "publish", "updated"]


class PlaylistRepository(PlaylistInterface):
    def queryset(self) -> QuerySet[Playlist]:
        return Playlist.objects.prefetch_related(Prefetch("playlist_audios", queryset=PlaylistAudio.objects.order_by("sequence")))

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.author_id:
            q_list.append(Q(author_id=filter.author_id))
        if filter.publish is not None:
            q_list.append(Q(publish=filter.publish))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Playlist.objects.filter(*q_list).order_by(order_by_key, "id" if sort.is_asc else "-id")
        qs = page_queryset(qs, page)

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[PlaylistData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[PlaylistData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]

        with transaction.atomic():
            new_ids = get_save_new_ids(models, PLAYLIST_FIELDS)
            playlist_ids = [model.id for model in models]
            PlaylistAudio.objects.filter(playlist_id__in=playlist_ids).delete()
            PlaylistAudio.objects.bulk_create([
                PlaylistAudio(playlist_id=model.id, audio_id=audio_id, sequence=seq)
                for obj, model in zip(objs, models)
                for seq, audio_id in enumerate(obj.audio_ids)
            ])

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        if len(ids) == 0:
            return Result.ok(None)
        Playlist.objects.filter(id__in=ids).delete()
        return Result.ok(None)
