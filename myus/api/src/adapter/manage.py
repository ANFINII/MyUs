from django.http import HttpRequest
from ninja import File, Form, Router, UploadedFile
from api.modules.logger import log
from api.src.adapter.media import convert_videos, convert_musics, convert_blogs, convert_comics, convert_pictures, convert_chats
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.types.schema.advertise import AdvertiseIn, AdvertiseListOut, AdvertiseOut, AdvertiseUpdateIn
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.media.input import BulkDeleteIn, VideoUpdateIn, MusicUpdateIn, BlogUpdateIn, ComicUpdateIn, PictureUpdateIn, ChatUpdateIn
from api.src.types.schema.media.output import MediaCreateOut, VideoOut, MusicOut, BlogOut, ComicOut, PictureOut, ChatOut
from api.src.types.schema.media.output import VideoListOut, MusicListOut, BlogListOut, ComicListOut, PictureListOut, ChatListOut
from api.src.domain.interface.media.index import PAGE_SIZE
from api.src.usecase.auth import auth_check
from api.src.usecase.manage.advertise import get_manage_advertises, get_manage_advertise, create_manage_advertise, update_manage_advertise, delete_manage_advertise
from api.src.usecase.manage.media import (
    get_manage_videos, get_manage_video, update_manage_video, delete_manage_video,
    get_manage_musics, get_manage_music, update_manage_music, delete_manage_music,
    get_manage_blogs, get_manage_blog, update_manage_blog, delete_manage_blog,
    get_manage_comics, get_manage_comic, update_manage_comic, delete_manage_comic,
    get_manage_pictures, get_manage_picture, update_manage_picture, delete_manage_picture,
    get_manage_chats, get_manage_chat, update_manage_chat, delete_manage_chat,
)


class ManageVideoAPI:
    """ManageVideoAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: VideoListOut, 401: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: int = PAGE_SIZE, offset: int = 0):
        log.info("ManageVideoAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        objs, total = get_manage_videos(user_id, search, channel, limit, offset)
        return 200, VideoListOut(datas=convert_videos(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: VideoOut, 401: ErrorOut, 404: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageVideoAPI get", ulid=ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        obj = get_manage_video(user_id, ulid)
        if obj is None:
            return 404, ErrorOut(message="Video not found")

        return 200, convert_videos([obj])[0]

    @staticmethod
    @router.put("/{ulid}", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: VideoUpdateIn = Form(...), image: UploadedFile | None = File(None)):
        log.info("ManageVideoAPI put", ulid=ulid, input=input, image=image)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_manage_video(user_id, ulid, input, image):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageVideoAPI delete", ulids=input.ulids)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not delete_manage_video(user_id, input.ulids):
            return 400, ErrorOut(message="削除に失敗しました!")

        return 204, ErrorOut(message="削除しました!")


class ManageMusicAPI:
    """ManageMusicAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: MusicListOut, 401: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: int = PAGE_SIZE, offset: int = 0):
        log.info("ManageMusicAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        objs, total = get_manage_musics(user_id, search, channel, limit, offset)
        return 200, MusicListOut(datas=convert_musics(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: MusicOut, 401: ErrorOut, 404: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageMusicAPI get", ulid=ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        obj = get_manage_music(user_id, ulid)
        if obj is None:
            return 404, ErrorOut(message="Music not found")

        return 200, convert_musics([obj])[0]

    @staticmethod
    @router.put("/{ulid}", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: MusicUpdateIn):
        log.info("ManageMusicAPI put", ulid=ulid, input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_manage_music(user_id, ulid, input):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageMusicAPI delete", ulids=input.ulids)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not delete_manage_music(user_id, input.ulids):
            return 400, ErrorOut(message="削除に失敗しました!")

        return 204, ErrorOut(message="削除しました!")


class ManageBlogAPI:
    """ManageBlogAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: BlogListOut, 401: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: int = PAGE_SIZE, offset: int = 0):
        log.info("ManageBlogAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        objs, total = get_manage_blogs(user_id, search, channel, limit, offset)
        return 200, BlogListOut(datas=convert_blogs(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: BlogOut, 401: ErrorOut, 404: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageBlogAPI get", ulid=ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        obj = get_manage_blog(user_id, ulid)
        if obj is None:
            return 404, ErrorOut(message="Blog not found")

        return 200, convert_blogs([obj])[0]

    @staticmethod
    @router.put("/{ulid}", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: BlogUpdateIn = Form(...), image: UploadedFile | None = File(None)):
        log.info("ManageBlogAPI put", ulid=ulid, input=input, image=image)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_manage_blog(user_id, ulid, input, image):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageBlogAPI delete", ulids=input.ulids)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not delete_manage_blog(user_id, input.ulids):
            return 400, ErrorOut(message="削除に失敗しました!")

        return 204, ErrorOut(message="削除しました!")


class ManageComicAPI:
    """ManageComicAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: ComicListOut, 401: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: int = PAGE_SIZE, offset: int = 0):
        log.info("ManageComicAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        objs, total = get_manage_comics(user_id, search, channel, limit, offset)
        return 200, ComicListOut(datas=convert_comics(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: ComicOut, 401: ErrorOut, 404: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageComicAPI get", ulid=ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        obj = get_manage_comic(user_id, ulid)
        if obj is None:
            return 404, ErrorOut(message="Comic not found")

        return 200, convert_comics([obj])[0]

    @staticmethod
    @router.put("/{ulid}", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: ComicUpdateIn = Form(...), image: UploadedFile | None = File(None)):
        log.info("ManageComicAPI put", ulid=ulid, input=input, image=image)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_manage_comic(user_id, ulid, input, image):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageComicAPI delete", ulids=input.ulids)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not delete_manage_comic(user_id, input.ulids):
            return 400, ErrorOut(message="削除に失敗しました!")

        return 204, ErrorOut(message="削除しました!")


class ManagePictureAPI:
    """ManagePictureAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: PictureListOut, 401: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: int = PAGE_SIZE, offset: int = 0):
        log.info("ManagePictureAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        objs, total = get_manage_pictures(user_id, search, channel, limit, offset)
        return 200, PictureListOut(datas=convert_pictures(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: PictureOut, 401: ErrorOut, 404: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManagePictureAPI get", ulid=ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        obj = get_manage_picture(user_id, ulid)
        if obj is None:
            return 404, ErrorOut(message="Picture not found")

        return 200, convert_pictures([obj])[0]

    @staticmethod
    @router.put("/{ulid}", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: PictureUpdateIn = Form(...), image: UploadedFile | None = File(None)):
        log.info("ManagePictureAPI put", ulid=ulid, input=input, image=image)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_manage_picture(user_id, ulid, input, image):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManagePictureAPI delete", ulids=input.ulids)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not delete_manage_picture(user_id, input.ulids):
            return 400, ErrorOut(message="削除に失敗しました!")

        return 204, ErrorOut(message="削除しました!")


class ManageChatAPI:
    """ManageChatAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: ChatListOut, 401: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: int = PAGE_SIZE, offset: int = 0):
        log.info("ManageChatAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        objs, total = get_manage_chats(user_id, search, channel, limit, offset)
        return 200, ChatListOut(datas=convert_chats(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: ChatOut, 401: ErrorOut, 404: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageChatAPI get", ulid=ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        obj = get_manage_chat(user_id, ulid)
        if obj is None:
            return 404, ErrorOut(message="Chat not found")

        return 200, convert_chats([obj])[0]

    @staticmethod
    @router.put("/{ulid}", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: ChatUpdateIn):
        log.info("ManageChatAPI put", ulid=ulid, input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_manage_chat(user_id, ulid, input):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageChatAPI delete", ulids=input.ulids)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not delete_manage_chat(user_id, input.ulids):
            return 400, ErrorOut(message="削除に失敗しました!")

        return 204, ErrorOut(message="削除しました!")


class ManageAdvertiseAPI:
    """ManageAdvertiseAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: AdvertiseListOut, 401: ErrorOut})
    def list(request: HttpRequest, search: str = "", limit: int = PAGE_SIZE, offset: int = 0):
        log.info("ManageAdvertiseAPI list", search=search, limit=limit, offset=offset)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        objs, total = get_manage_advertises(user_id, search, limit, offset)
        return 200, AdvertiseListOut(datas=convert_advertises(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: AdvertiseOut, 401: ErrorOut, 404: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageAdvertiseAPI get", ulid=ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        obj = get_manage_advertise(user_id, ulid)
        if obj is None:
            return 404, ErrorOut(message="Advertise not found")

        return 200, convert_advertises([obj])[0]

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 400: ErrorOut, 401: ErrorOut})
    def post(request: HttpRequest, input: AdvertiseIn = Form(...), image: UploadedFile = File(...), video: UploadedFile | None = File(None)):
        log.info("ManageAdvertiseAPI post", input=input, image=image, video=video)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        obj = create_manage_advertise(user_id, input, image, video)
        if obj is None:
            return 400, ErrorOut(message="作成に失敗しました!")

        return 201, MediaCreateOut(ulid=obj.ulid)

    @staticmethod
    @router.put("/{ulid}", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: AdvertiseUpdateIn = Form(...), image: UploadedFile | None = File(None), video: UploadedFile | None = File(None)):
        log.info("ManageAdvertiseAPI put", ulid=ulid, input=input, image=image, video=video)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_manage_advertise(user_id, ulid, input, image, video):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageAdvertiseAPI delete", ulids=input.ulids)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not delete_manage_advertise(user_id, input.ulids):
            return 400, ErrorOut(message="削除に失敗しました!")

        return 204, ErrorOut(message="削除しました!")


def convert_advertises(objs: list[AdvertiseData]) -> list[AdvertiseOut]:
    return [
        AdvertiseOut(
            ulid=o.ulid,
            title=o.title,
            url=o.url,
            content=o.content,
            image=o.image,
            video=o.video,
            read=o.read,
            type=o.type,
            period=o.period,
            publish=o.publish,
            created=o.created,
            updated=o.updated,
        )
        for o in objs
    ]
