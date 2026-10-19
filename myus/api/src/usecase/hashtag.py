import re
from api.modules.logger import log
from api.src.domain.interface.hashtag.data import HashtagData
from api.src.domain.interface.hashtag.interface import FilterOption as HashtagFilterOption, HashtagInterface, SortOption as HashtagSortOption, SortType as HashtagSortType
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption
from api.src.domain.interface.ng_word.interface import FilterOption as NgWordFilterOption, NgWordInterface, SortOption as NgWordSortOption
from api.src.injectors.container import injector
from api.src.types.dto.hashtag import HashtagDTO
from api.utils.common.result import FatalError, NotFoundError, Result
from api.utils.enum.media import MediaType
from api.utils.functions.media import get_media_repository


HASHTAG_MAX_LENGTH = 30
ALLOWED_PATTERN = re.compile(r"^[ぁ-んァ-ヶー一-龯a-zA-Z]+$")


def normalize_name(name: str) -> str:
    return name.strip().lstrip("#").lower()


def validate_name(name: str, ng_words: list[str]) -> bool:
    if len(name) == 0:
        return False
    if len(name) > HASHTAG_MAX_LENGTH:
        return False
    if ALLOWED_PATTERN.match(name) is None:
        return False
    if any(ng in name for ng in ng_words):
        return False
    return True


@Result.shield_exception()
def get_master_hashtags() -> Result[list[HashtagDTO], FatalError]:
    repo = injector.get(HashtagInterface)
    ids_ret = repo.get_ids(HashtagFilterOption(), HashtagSortOption(is_asc=True, sort_type=HashtagSortType.NAME))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    hashtags_ret = repo.bulk_get(ids)
    if hashtags_ret.is_err:
        return Result.err(hashtags_ret.err_value)

    hashtags = hashtags_ret.ok_value
    return Result.ok([HashtagDTO(ulid=h.ulid, name=h.name) for h in hashtags])


@Result.shield_exception()
def get_ng_words() -> Result[list[str], FatalError]:
    repo = injector.get(NgWordInterface)
    ids_ret = repo.get_ids(NgWordFilterOption(), NgWordSortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    ng_words_ret = repo.bulk_get(ids)
    if ng_words_ret.is_err:
        return Result.err(ng_words_ret.err_value)

    ng_words = ng_words_ret.ok_value
    return Result.ok([n.word for n in ng_words])


@Result.shield_exception()
def update_media_hashtags(user_id: int, media_type: MediaType, media_ulid: str, hashtags: list[HashtagDTO]) -> Result[None, NotFoundError | FatalError]:
    media_repo = get_media_repository(media_type)
    hashtag_repo = injector.get(HashtagInterface)
    media_ids_ret = media_repo.get_ids(FilterOption(ulid=media_ulid), ExcludeOption(), SortOption(), PageOption())
    if media_ids_ret.is_err:
        return Result.err(media_ids_ret.err_value)

    media_ids = media_ids_ret.ok_value
    if len(media_ids) == 0:
        log.error("Media not found", media_type=media_type.value, media_ulid=media_ulid)
        return Result.err(NotFoundError("保存に失敗しました!"))

    medias_ret = media_repo.bulk_get(media_ids)
    if medias_ret.is_err:
        return Result.err(medias_ret.err_value)

    medias = medias_ret.ok_value
    media = medias[0]
    if media.channel.owner_id != user_id:
        log.error("Media owner mismatch", media_type=media_type.value, media_ulid=media_ulid, user_id=user_id)
        return Result.err(NotFoundError("保存に失敗しました!"))

    ulids = [h.ulid for h in hashtags if h.ulid]
    ulid_data_map: dict[str, HashtagData] = {}
    if len(ulids) > 0:
        existing_ids_ret = hashtag_repo.get_ids(HashtagFilterOption(ulids=ulids), HashtagSortOption())
        if existing_ids_ret.is_err:
            return Result.err(existing_ids_ret.err_value)

        existing_ids = existing_ids_ret.ok_value
        existing_hashtags_ret = hashtag_repo.bulk_get(existing_ids)
        if existing_hashtags_ret.is_err:
            return Result.err(existing_hashtags_ret.err_value)

        existing_hashtags = existing_hashtags_ret.ok_value
        for tag in existing_hashtags:
            ulid_data_map[tag.ulid] = tag

    ng_words_ret = get_ng_words()
    if ng_words_ret.is_err:
        return Result.err(ng_words_ret.err_value)

    ng_words = ng_words_ret.ok_value
    seen_name: set[str] = set()
    update_hashtags: list[HashtagData] = []

    for h in hashtags:
        if h.ulid and h.ulid in ulid_data_map:
            existing = ulid_data_map[h.ulid]
            if existing.name in seen_name:
                continue
            seen_name.add(existing.name)
            update_hashtags.append(existing)
            continue

        normalized = normalize_name(h.name)
        if not validate_name(normalized, ng_words):
            continue
        if normalized in seen_name:
            continue
        seen_name.add(normalized)
        update_hashtags.append(HashtagData(id=0, ulid="", name=normalized))

    save_ret = hashtag_repo.bulk_save(media_type, media.id, update_hashtags)
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)
