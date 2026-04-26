import re
from api.modules.logger import log
from api.src.domain.interface.hashtag.data import HashtagData
from api.src.domain.interface.hashtag.interface import FilterOption as HashtagFilterOption, HashtagInterface, SortOption as HashtagSortOption
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption
from api.src.domain.interface.ng_word.interface import FilterOption as NgWordFilterOption, NgWordInterface, SortOption as NgWordSortOption
from api.src.injectors.container import injector
from api.src.types.dto.hashtag import HashtagDTO
from api.utils.enum.index import MediaType
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


def get_ng_words() -> list[str]:
    repo = injector.get(NgWordInterface)
    ids = repo.get_ids(NgWordFilterOption(), NgWordSortOption())
    return [n.word for n in repo.bulk_get(ids)]


def update_media_hashtags(user_id: int, media_type: MediaType, media_ulid: str, hashtags: list[HashtagDTO]) -> bool:
    media_repo = get_media_repository(media_type)
    hashtag_repo = injector.get(HashtagInterface)
    media_ids = media_repo.get_ids(FilterOption(ulid=media_ulid), ExcludeOption(), SortOption(), PageOption())
    if len(media_ids) == 0:
        log.error("Media not found", media_type=media_type.value, media_ulid=media_ulid)
        return False

    media = media_repo.bulk_get(media_ids)[0]
    if media.channel.owner_id != user_id:
        log.error("Media owner mismatch", media_type=media_type.value, media_ulid=media_ulid, user_id=user_id)
        return False

    ulids = [h.ulid for h in hashtags if h.ulid]
    ulid_data_map: dict[str, HashtagData] = {}
    if len(ulids) > 0:
        existing_ids = hashtag_repo.get_ids(HashtagFilterOption(ulids=ulids), HashtagSortOption())
        for tag in hashtag_repo.bulk_get(existing_ids):
            ulid_data_map[tag.ulid] = tag

    ng_words = get_ng_words()
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

    try:
        hashtag_repo.bulk_save(media_type, media.id, update_hashtags)
        return True
    except Exception as e:
        log.error("update_media_hashtags error", exc=e)
        return False
