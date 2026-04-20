from dataclasses import replace
from datetime import date
from ninja import UploadedFile
from api.modules.logger import log
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.comic.data import ComicData
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.picture.data import PictureData
from api.src.domain.interface.media.picture.interface import PictureInterface
from api.src.domain.interface.media.blog.data import BlogData
from api.src.domain.interface.media.blog.interface import BlogInterface
from api.src.domain.interface.media.chat.data import ChatData
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.media.index import FilterOption, SortOption, ExcludeOption
from api.src.injectors.container import injector
from api.src.types.schema.media.input import BlogUpdateIn, ChatUpdateIn, ComicUpdateIn, MusicUpdateIn, PictureUpdateIn, VideoUpdateIn
from api.utils.enum.index import ImageUpload
from api.utils.functions.index import create_url
from api.utils.functions.media import save_upload


def get_manage_videos(user_id: int, search: str) -> list[VideoData]:
    repository = injector.get(VideoInterface)
    filter = FilterOption(search=search, owner_id=user_id)
    ids = repository.get_ids(filter, ExcludeOption(), SortOption())
    objs = repository.bulk_get(ids=ids)

    data = [replace(o,
        image=create_url(o.image),
        video=create_url(o.video),
        convert=create_url(o.convert),
    ) for o in objs]

    return data


def get_manage_video(user_id: int, ulid: str) -> VideoData | None:
    repository = injector.get(VideoInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.info("Video not found", ulid=ulid, user_id=user_id)
        return None

    obj = repository.bulk_get(ids)[0]
    return replace(obj,
        image=create_url(obj.image),
        video=create_url(obj.video),
        convert=create_url(obj.convert),
    )


def update_manage_video(user_id: int, ulid: str, input: VideoUpdateIn, image: UploadedFile | None = None) -> bool:
    repository = injector.get(VideoInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.error("Video not found", ulid=ulid)
        return False

    obj = repository.bulk_get(ids)[0]
    if obj.channel.owner_id != user_id:
        log.error("Video owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return False

    update_data = replace(obj, title=input.title, content=input.content, publish=input.publish)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.VIDEO, obj.channel.ulid))

    try:
        repository.bulk_save([update_data])
        return True
    except Exception as e:
        log.error("update_manage_video error", exc=e)
        return False


def delete_manage_video(user_id: int, ulids: list[str]) -> bool:
    repository = injector.get(VideoInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
        if len(ids) == 0:
            log.error("Video not found or owner mismatch", ulid=ulid, user_id=user_id)
            return False
        delete_ids.append(ids[0])

    try:
        repository.bulk_delete(delete_ids)
        return True
    except Exception as e:
        log.error("delete_manage_video error", exc=e)
        return False


def get_manage_musics(user_id: int, search: str) -> list[MusicData]:
    repository = injector.get(MusicInterface)
    filter = FilterOption(search=search, owner_id=user_id)
    ids = repository.get_ids(filter, ExcludeOption(), SortOption())
    objs = repository.bulk_get(ids=ids)

    data = [replace(o, music=create_url(o.music)) for o in objs]
    return data


def get_manage_music(user_id: int, ulid: str) -> MusicData | None:
    repository = injector.get(MusicInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.info("Music not found", ulid=ulid, user_id=user_id)
        return None

    obj = repository.bulk_get(ids)[0]
    return replace(obj, music=create_url(obj.music))


def update_manage_music(user_id: int, ulid: str, input: MusicUpdateIn) -> bool:
    repository = injector.get(MusicInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.error("Music not found", ulid=ulid)
        return False

    obj = repository.bulk_get(ids)[0]
    if obj.channel.owner_id != user_id:
        log.error("Music owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return False

    update_data = replace(obj, title=input.title, content=input.content, lyric=input.lyric, download=input.download, publish=input.publish)
    try:
        repository.bulk_save([update_data])
        return True
    except Exception as e:
        log.error("update_manage_music error", exc=e)
        return False


def delete_manage_music(user_id: int, ulids: list[str]) -> bool:
    repository = injector.get(MusicInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
        if len(ids) == 0:
            log.error("Music not found or owner mismatch", ulid=ulid, user_id=user_id)
            return False
        delete_ids.append(ids[0])

    try:
        repository.bulk_delete(delete_ids)
        return True
    except Exception as e:
        log.error("delete_manage_music error", exc=e)
        return False


def get_manage_comics(user_id: int, search: str) -> list[ComicData]:
    repository = injector.get(ComicInterface)
    filter = FilterOption(search=search, owner_id=user_id)
    ids = repository.get_ids(filter, ExcludeOption(), SortOption())
    objs = repository.bulk_get(ids=ids)

    data = [replace(o,
        image=create_url(o.image),
        pages=[create_url(p) for p in o.pages],
    ) for o in objs]
    return data


def get_manage_comic(user_id: int, ulid: str) -> ComicData | None:
    repository = injector.get(ComicInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.info("Comic not found", ulid=ulid, user_id=user_id)
        return None

    obj = repository.bulk_get(ids)[0]
    return replace(obj,
        image=create_url(obj.image),
        pages=[create_url(p) for p in obj.pages],
    )


def update_manage_comic(user_id: int, ulid: str, input: ComicUpdateIn, image: UploadedFile | None = None) -> bool:
    repository = injector.get(ComicInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.error("Comic not found", ulid=ulid)
        return False

    obj = repository.bulk_get(ids)[0]
    if obj.channel.owner_id != user_id:
        log.error("Comic owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return False

    update_data = replace(obj, title=input.title, content=input.content, publish=input.publish)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.COMIC, obj.channel.ulid))

    try:
        repository.bulk_save([update_data])
        return True
    except Exception as e:
        log.error("update_manage_comic error", exc=e)
        return False


def delete_manage_comic(user_id: int, ulids: list[str]) -> bool:
    repository = injector.get(ComicInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
        if len(ids) == 0:
            log.error("Comic not found or owner mismatch", ulid=ulid, user_id=user_id)
            return False
        delete_ids.append(ids[0])

    try:
        repository.bulk_delete(delete_ids)
        return True
    except Exception as e:
        log.error("delete_manage_comic error", exc=e)
        return False


def get_manage_pictures(user_id: int, search: str) -> list[PictureData]:
    repository = injector.get(PictureInterface)
    filter = FilterOption(search=search, owner_id=user_id)
    ids = repository.get_ids(filter, ExcludeOption(), SortOption())
    objs = repository.bulk_get(ids=ids)

    data = [replace(o, image=create_url(o.image)) for o in objs]
    return data


def get_manage_picture(user_id: int, ulid: str) -> PictureData | None:
    repository = injector.get(PictureInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.info("Picture not found", ulid=ulid, user_id=user_id)
        return None

    obj = repository.bulk_get(ids)[0]
    return replace(obj, image=create_url(obj.image))


def update_manage_picture(user_id: int, ulid: str, input: PictureUpdateIn, image: UploadedFile | None = None) -> bool:
    repository = injector.get(PictureInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.error("Picture not found", ulid=ulid)
        return False

    obj = repository.bulk_get(ids)[0]
    if obj.channel.owner_id != user_id:
        log.error("Picture owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return False

    update_data = replace(obj, title=input.title, content=input.content, publish=input.publish)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.PICTURE, obj.channel.ulid))

    try:
        repository.bulk_save([update_data])
        return True
    except Exception as e:
        log.error("update_manage_picture error", exc=e)
        return False


def delete_manage_picture(user_id: int, ulids: list[str]) -> bool:
    repository = injector.get(PictureInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
        if len(ids) == 0:
            log.error("Picture not found or owner mismatch", ulid=ulid, user_id=user_id)
            return False
        delete_ids.append(ids[0])

    try:
        repository.bulk_delete(delete_ids)
        return True
    except Exception as e:
        log.error("delete_manage_picture error", exc=e)
        return False


def get_manage_blogs(user_id: int, search: str) -> list[BlogData]:
    repository = injector.get(BlogInterface)
    filter = FilterOption(search=search, owner_id=user_id)
    ids = repository.get_ids(filter, ExcludeOption(), SortOption())
    objs = repository.bulk_get(ids=ids)

    data = [replace(o, image=create_url(o.image)) for o in objs]
    return data


def get_manage_blog(user_id: int, ulid: str) -> BlogData | None:
    repository = injector.get(BlogInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.info("Blog not found", ulid=ulid, user_id=user_id)
        return None

    obj = repository.bulk_get(ids)[0]
    return replace(obj, image=create_url(obj.image))


def update_manage_blog(user_id: int, ulid: str, input: BlogUpdateIn, image: UploadedFile | None = None) -> bool:
    repository = injector.get(BlogInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.error("Blog not found", ulid=ulid)
        return False

    obj = repository.bulk_get(ids)[0]
    if obj.channel.owner_id != user_id:
        log.error("Blog owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return False

    update_data = replace(obj, title=input.title, content=input.content, richtext=input.richtext, publish=input.publish)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.BLOG, obj.channel.ulid))

    try:
        repository.bulk_save([update_data])
        return True
    except Exception as e:
        log.error("update_manage_blog error", exc=e)
        return False


def delete_manage_blog(user_id: int, ulids: list[str]) -> bool:
    repository = injector.get(BlogInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
        if len(ids) == 0:
            log.error("Blog not found or owner mismatch", ulid=ulid, user_id=user_id)
            return False
        delete_ids.append(ids[0])

    try:
        repository.bulk_delete(delete_ids)
        return True
    except Exception as e:
        log.error("delete_manage_blog error", exc=e)
        return False


def get_manage_chats(user_id: int, search: str) -> list[ChatData]:
    repository = injector.get(ChatInterface)
    filter = FilterOption(search=search, owner_id=user_id)
    ids = repository.get_ids(filter, ExcludeOption(), SortOption())
    return repository.bulk_get(ids=ids)


def get_manage_chat(user_id: int, ulid: str) -> ChatData | None:
    repository = injector.get(ChatInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.info("Chat not found", ulid=ulid, user_id=user_id)
        return None

    return repository.bulk_get(ids)[0]


def update_manage_chat(user_id: int, ulid: str, input: ChatUpdateIn) -> bool:
    repository = injector.get(ChatInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.error("Chat not found", ulid=ulid)
        return False

    obj = repository.bulk_get(ids)[0]
    if obj.channel.owner_id != user_id:
        log.error("Chat owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return False

    update_data = replace(obj, title=input.title, content=input.content, period=date.fromisoformat(input.period), publish=input.publish)
    try:
        repository.bulk_save([update_data])
        return True
    except Exception as e:
        log.error("update_manage_chat error", exc=e)
        return False


def delete_manage_chat(user_id: int, ulids: list[str]) -> bool:
    repository = injector.get(ChatInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
        if len(ids) == 0:
            log.error("Chat not found or owner mismatch", ulid=ulid, user_id=user_id)
            return False
        delete_ids.append(ids[0])

    try:
        repository.bulk_delete(delete_ids)
        return True
    except Exception as e:
        log.error("delete_manage_chat error", exc=e)
        return False
