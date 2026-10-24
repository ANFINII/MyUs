from datetime import datetime, time
from typing import assert_never
from django.http import HttpRequest
from ninja import File, Form, Router, UploadedFile
from api.modules.logger import log
from api.src.adapter.auth import auth_check
from api.src.types.dto.comment import CommentDTO, ReplyDTO
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.blog.data import BlogData
from api.src.domain.interface.media.comic.data import ComicData
from api.src.domain.interface.media.picture.data import PictureData
from api.src.domain.interface.media.chat.data import ChatData
from api.src.domain.interface.hashtag.data import HashtagData
from api.src.domain.interface.channel.data import ChannelData
from api.utils.functions.index import create_url, get_client_ip
from api.src.types.dto.message import MessageDTO
from api.src.types.dto.user import AuthorDTO, MediaUserDTO
from api.src.types.schema.common import ErrorOut, ErrorType, Limit, Offset
from api.src.types.schema.comment import CommentOut, ReplyOut
from api.src.types.schema.media.input import VideoIn, MusicIn, BlogIn, ComicIn, PictureIn, ChatIn, MediaReadIn
from api.src.types.schema.media.output import HomeOut, VideoOut, MusicOut, BlogOut, ComicOut, PictureOut, ChatOut, MediaCreateOut, MediaReadOut, HashtagOut
from api.src.types.schema.media.output import VideoListOut, MusicListOut, BlogListOut, ComicListOut, PictureListOut, ChatListOut
from api.src.types.schema.media.output import VideoDetailOut, MusicDetailOut, BlogDetailOut, ComicDetailOut, PictureDetailOut, ChatDetailOut
from api.src.types.schema.media.output import VideoDetailsOut, MusicDetailsOut, BlogDetailsOut, ComicDetailsOut, PictureDetailsOut, ChatDetailsOut
from api.src.types.schema.message import MessageOut
from api.src.types.schema.channel import ChannelOut
from api.src.types.schema.user import AuthorOut, MediaUserOut
from api.src.domain.interface.media.index import PAGE_SIZE
from api.src.usecase.media import create_video, create_music, create_blog, create_comic, create_picture, create_chat
from api.src.usecase.media import get_home, get_recommend, get_videos, get_musics, get_blogs, get_comics, get_pictures, get_chats
from api.src.usecase.media import get_video_detail, get_music_detail, get_blog_detail, get_comic_detail, get_picture_detail, get_chat_detail
from api.src.usecase.media import increment_media_read
from api.utils.common.result import FatalError, ForbiddenError, NotFoundError, ValidationError


class HomeAPI:
    """HomeAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: HomeOut, 500: ErrorOut})
    def get(request: HttpRequest, search: str = ""):
        log.info("HomeAPI get", search=search)

        ret = get_home(8, search)
        if ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        home = ret.ok_value
        data = HomeOut(
            videos=convert_videos(home.videos),
            musics=convert_musics(home.musics),
            blogs=convert_blogs(home.blogs),
            comics=convert_comics(home.comics),
            pictures=convert_pictures(home.pictures),
            chats=convert_chats(home.chats),
        )

        return 200, data


class RecommendAPI:
    """RecommendAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: HomeOut, 500: ErrorOut})
    def get(request: HttpRequest, search: str = ""):
        log.info("RecommendAPI get", search=search)

        ret = get_recommend(8, search)
        if ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        recommend = ret.ok_value
        data = HomeOut(
            videos=convert_videos(recommend.videos),
            musics=convert_musics(recommend.musics),
            blogs=convert_blogs(recommend.blogs),
            comics=convert_comics(recommend.comics),
            pictures=convert_pictures(recommend.pictures),
            chats=convert_chats(recommend.chats),
        )

        return 200, data


class VideoAPI:
    """VideoAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={200: MediaCreateOut, 400: ErrorOut, 500: ErrorOut})
    def create(
        request: HttpRequest,
        input: VideoIn = Form(...),
        image: UploadedFile = File(...),
        video: UploadedFile = File(...),
    ):
        log.info("VideoAPI create", input=input, image=image, video=video)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        obj_ret = create_video(user_id=user_id, input=input, image=image, video=video)
        if obj_ret.is_err:
            message = obj_ret.err_value.message
            match obj_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(obj_ret.err_value)

        obj = obj_ret.ok_value
        data = MediaCreateOut(ulid=obj.ulid)
        return 200, data

    @staticmethod
    @router.get("", response={200: VideoListOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("VideoAPI list", search=search, limit=limit, offset=offset)
        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        videos_ret = get_videos(search, user_id=user_id, limit=limit, offset=offset)
        if videos_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = videos_ret.ok_value
        data = VideoListOut(items=convert_videos(objs), total=total)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: VideoDetailsOut, 400: ErrorOut, 500: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("VideoAPI detail", ulid=ulid, search=search)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        detail_ret = get_video_detail(user_id=user_id, ulid=ulid, publish=True)
        if detail_ret.is_err:
            message = detail_ret.err_value.message
            match detail_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(detail_ret.err_value)

        obj = detail_ret.ok_value

        list_ret = get_videos(search, obj.id)
        if list_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, _ = list_ret.ok_value

        data = VideoDetailsOut(
            detail=VideoDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                image=obj.image,
                video=obj.video,
                convert=obj.convert,
                comments=convert_comments(obj.comments),
                hashtags=convert_hashtags(obj.hashtags),
                read=obj.read,
                like=obj.like,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                channel=convert_channel(obj.channel),
                mediaUser=convert_media_user(obj.mediaUser),
            ),
            list=convert_videos(objs),
        )

        return 200, data


class MusicAPI:
    """MusicAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={200: MediaCreateOut, 400: ErrorOut, 500: ErrorOut})
    def create(request: HttpRequest, input: MusicIn = Form(...), music: UploadedFile = File(...)):
        log.info("MusicAPI create", input=input, music=music)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        obj_ret = create_music(user_id=user_id, input=input, music=music)
        if obj_ret.is_err:
            message = obj_ret.err_value.message
            match obj_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(obj_ret.err_value)

        obj = obj_ret.ok_value
        data = MediaCreateOut(ulid=obj.ulid)
        return 200, data

    @staticmethod
    @router.get("", response={200: MusicListOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("MusicAPI list", search=search, limit=limit, offset=offset)
        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        musics_ret = get_musics(search, user_id=user_id, limit=limit, offset=offset)
        if musics_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = musics_ret.ok_value
        data = MusicListOut(items=convert_musics(objs), total=total)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: MusicDetailsOut, 400: ErrorOut, 500: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("MusicAPI detail", ulid=ulid, search=search)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        detail_ret = get_music_detail(user_id=user_id, ulid=ulid, publish=True)
        if detail_ret.is_err:
            message = detail_ret.err_value.message
            match detail_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(detail_ret.err_value)

        obj = detail_ret.ok_value

        list_ret = get_musics(search, obj.id)
        if list_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, _ = list_ret.ok_value

        data = MusicDetailsOut(
            detail=MusicDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                lyric=obj.lyric,
                music=obj.music,
                download=obj.download,
                comments=convert_comments(obj.comments),
                hashtags=convert_hashtags(obj.hashtags),
                read=obj.read,
                like=obj.like,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                channel=convert_channel(obj.channel),
                mediaUser=convert_media_user(obj.mediaUser),
            ),
            list=convert_musics(objs),
        )

        return 200, data


class BlogAPI:
    """BlogAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={200: MediaCreateOut, 400: ErrorOut, 500: ErrorOut})
    def create(request: HttpRequest, input: BlogIn = Form(...), image: UploadedFile = File(...)):
        log.info("BlogAPI create", input=input, image=image)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        obj_ret = create_blog(user_id=user_id, input=input, image=image)
        if obj_ret.is_err:
            message = obj_ret.err_value.message
            match obj_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(obj_ret.err_value)

        obj = obj_ret.ok_value
        data = MediaCreateOut(ulid=obj.ulid)
        return 200, data

    @staticmethod
    @router.get("", response={200: BlogListOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("BlogAPI list", search=search, limit=limit, offset=offset)
        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        blogs_ret = get_blogs(search, user_id=user_id, limit=limit, offset=offset)
        if blogs_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = blogs_ret.ok_value
        data = BlogListOut(items=convert_blogs(objs), total=total)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: BlogDetailsOut, 400: ErrorOut, 500: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("BlogAPI detail", ulid=ulid, search=search)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        detail_ret = get_blog_detail(user_id=user_id, ulid=ulid, publish=True)
        if detail_ret.is_err:
            message = detail_ret.err_value.message
            match detail_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(detail_ret.err_value)

        obj = detail_ret.ok_value

        list_ret = get_blogs(search, obj.id)
        if list_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, _ = list_ret.ok_value

        data = BlogDetailsOut(
            detail=BlogDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                richtext=obj.richtext,
                is_promotion=obj.is_promotion,
                image=obj.image,
                comments=convert_comments(obj.comments),
                hashtags=convert_hashtags(obj.hashtags),
                read=obj.read,
                like=obj.like,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                channel=convert_channel(obj.channel),
                mediaUser=convert_media_user(obj.mediaUser),
            ),
            list=convert_blogs(objs),
        )

        return 200, data


class ComicAPI:
    """ComicAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={200: MediaCreateOut, 400: ErrorOut, 500: ErrorOut})
    def create(request: HttpRequest, input: ComicIn = Form(...), image: UploadedFile = File(...), pages: list[UploadedFile] = File(...)):
        log.info("ComicAPI create", input=input, image=image, pages=pages)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        obj_ret = create_comic(user_id=user_id, input=input, image=image, pages=pages)
        if obj_ret.is_err:
            message = obj_ret.err_value.message
            match obj_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(obj_ret.err_value)

        obj = obj_ret.ok_value
        data = MediaCreateOut(ulid=obj.ulid)
        return 200, data

    @staticmethod
    @router.get("", response={200: ComicListOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("ComicAPI list", search=search, limit=limit, offset=offset)
        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        comics_ret = get_comics(search, user_id=user_id, limit=limit, offset=offset)
        if comics_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = comics_ret.ok_value
        data = ComicListOut(items=convert_comics(objs), total=total)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: ComicDetailsOut, 400: ErrorOut, 500: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("ComicAPI detail", ulid=ulid, search=search)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        detail_ret = get_comic_detail(user_id=user_id, ulid=ulid, publish=True)
        if detail_ret.is_err:
            message = detail_ret.err_value.message
            match detail_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(detail_ret.err_value)

        obj = detail_ret.ok_value

        list_ret = get_comics(search, obj.id)
        if list_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, _ = list_ret.ok_value

        data = ComicDetailsOut(
            detail=ComicDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                image=obj.image,
                pages=obj.pages,
                comments=convert_comments(obj.comments),
                hashtags=convert_hashtags(obj.hashtags),
                read=obj.read,
                like=obj.like,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                channel=convert_channel(obj.channel),
                mediaUser=convert_media_user(obj.mediaUser),
            ),
            list=convert_comics(objs),
        )

        return 200, data


class PictureAPI:
    """PictureAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={200: MediaCreateOut, 400: ErrorOut, 500: ErrorOut})
    def create(request: HttpRequest, input: PictureIn = Form(...), image: UploadedFile = File(...)):
        log.info("PictureAPI create", input=input, image=image)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        obj_ret = create_picture(user_id=user_id, input=input, image=image)
        if obj_ret.is_err:
            message = obj_ret.err_value.message
            match obj_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(obj_ret.err_value)

        obj = obj_ret.ok_value
        data = MediaCreateOut(ulid=obj.ulid)
        return 200, data

    @staticmethod
    @router.get("", response={200: PictureListOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("PictureAPI list", search=search, limit=limit, offset=offset)
        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        pictures_ret = get_pictures(search, user_id=user_id, limit=limit, offset=offset)
        if pictures_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = pictures_ret.ok_value
        data = PictureListOut(items=convert_pictures(objs), total=total)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: PictureDetailsOut, 400: ErrorOut, 500: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("PictureAPI detail", ulid=ulid, search=search)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        detail_ret = get_picture_detail(user_id=user_id, ulid=ulid, publish=True)
        if detail_ret.is_err:
            message = detail_ret.err_value.message
            match detail_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(detail_ret.err_value)

        obj = detail_ret.ok_value

        list_ret = get_pictures(search, obj.id)
        if list_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, _ = list_ret.ok_value

        data = PictureDetailsOut(
            detail=PictureDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                image=obj.image,
                comments=convert_comments(obj.comments),
                hashtags=convert_hashtags(obj.hashtags),
                read=obj.read,
                like=obj.like,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                channel=convert_channel(obj.channel),
                mediaUser=convert_media_user(obj.mediaUser),
            ),
            list=convert_pictures(objs),
        )

        return 200, data


class ChatAPI:
    """ChatAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={200: MediaCreateOut, 400: ErrorOut, 500: ErrorOut})
    def create(request: HttpRequest, input: ChatIn = Form(...)):
        log.info("ChatAPI create", input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        obj_ret = create_chat(user_id=user_id, input=input)
        if obj_ret.is_err:
            message = obj_ret.err_value.message
            match obj_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(obj_ret.err_value)

        obj = obj_ret.ok_value
        data = MediaCreateOut(ulid=obj.ulid)
        return 200, data

    @staticmethod
    @router.get("", response={200: ChatListOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("ChatAPI list", search=search, limit=limit, offset=offset)
        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        chats_ret = get_chats(search, user_id=user_id, limit=limit, offset=offset)
        if chats_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = chats_ret.ok_value
        data = ChatListOut(items=convert_chats(objs), total=total)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: ChatDetailsOut, 400: ErrorOut, 500: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("ChatAPI detail", ulid=ulid, search=search)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        detail_ret = get_chat_detail(user_id=user_id, ulid=ulid, publish=True)
        if detail_ret.is_err:
            message = detail_ret.err_value.message
            match detail_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(detail_ret.err_value)

        obj = detail_ret.ok_value

        list_ret = get_chats(search, obj.id)
        if list_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, _ = list_ret.ok_value

        data = ChatDetailsOut(
            detail=ChatDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                thread=obj.thread,
                joined=obj.joined,
                period=datetime.combine(obj.period, time()),
                messages=convert_messages(obj.messages),
                hashtags=convert_hashtags(obj.hashtags),
                read=obj.read,
                like=obj.like,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                channel=convert_channel(obj.channel),
                mediaUser=convert_media_user(obj.mediaUser),
            ),
            list=convert_chats(objs),
        )

        return 200, data


class MediaReadAPI:
    """MediaReadAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={200: MediaReadOut, 400: ErrorOut, 500: ErrorOut})
    def post(request: HttpRequest, input: MediaReadIn):
        log.info("MediaReadAPI post", input=input)

        ret = increment_media_read(input.media_type, input.ulid, get_client_ip(request))
        if ret.is_err:
            message = ret.err_value.message
            match ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(ret.err_value)

        read = ret.ok_value
        return 200, MediaReadOut(read=read)


def convert_videos(objs: list[VideoData]) -> list[VideoOut]:
    data = [
        VideoOut(
            ulid=x.ulid,
            title=x.title,
            content=x.content,
            image=x.image,
            video=x.video,
            convert=x.convert,
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
            category_ulid=x.category_ulid,
        ) for x in objs
    ]
    return data


def convert_musics(objs: list[MusicData]) -> list[MusicOut]:
    data = [
        MusicOut(
            ulid=x.ulid,
            title=x.title,
            content=x.content,
            lyric=x.lyric,
            music=x.music,
            download=x.download,
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
            category_ulid=x.category_ulid,
        ) for x in objs
    ]
    return data


def convert_blogs(objs: list[BlogData]) -> list[BlogOut]:
    data = [
        BlogOut(
            ulid=x.ulid,
            title=x.title,
            content=x.content,
            image=x.image,
            richtext=x.richtext,
            is_promotion=x.is_promotion,
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
            category_ulid=x.category_ulid,
        ) for x in objs
    ]
    return data


def convert_comics(objs: list[ComicData]) -> list[ComicOut]:
    data = [
        ComicOut(
            ulid=x.ulid,
            title=x.title,
            content=x.content,
            image=x.image,
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
            category_ulid=x.category_ulid,
        ) for x in objs
    ]
    return data


def convert_pictures(objs: list[PictureData]) -> list[PictureOut]:
    data = [
        PictureOut(
            ulid=x.ulid,
            title=x.title,
            content=x.content,
            image=x.image,
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
            category_ulid=x.category_ulid,
        ) for x in objs
    ]
    return data


def convert_chats(objs: list[ChatData]) -> list[ChatOut]:
    data = [
        ChatOut(
            ulid=x.ulid,
            title=x.title,
            content=x.content,
            thread=x.thread_count,
            joined=x.joined_count,
            period=datetime.combine(x.period, time()),
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
            category_ulid=x.category_ulid,
        ) for x in objs
    ]
    return data


def convert_comments(objs: list[CommentDTO]) -> list[CommentOut]:
    data = [
        CommentOut(
            ulid=x.ulid,
            text=x.text,
            created=x.created,
            updated=x.updated,
            is_comment_like=x.is_comment_like,
            like_count=x.like_count,
            author=convert_author(x.author),
            replys=convert_replys(x.replys),
        ) for x in objs
    ]
    return data


def convert_replys(objs: list[ReplyDTO]) -> list[ReplyOut]:
    data = [
        ReplyOut(
            ulid=x.ulid,
            text=x.text,
            created=x.created,
            updated=x.updated,
            is_comment_like=x.is_comment_like,
            like_count=x.like_count,
            author=convert_author(x.author),
        ) for x in objs
    ]
    return data


def convert_messages(objs: list[MessageDTO]) -> list[MessageOut]:
    data = [
        MessageOut(
            ulid=m.ulid,
            text=m.text,
            reply_count=m.reply_count,
            created=m.created,
            updated=m.updated,
            author=convert_author(m.author),
        ) for m in objs
    ]
    return data


def convert_author(obj: AuthorDTO) -> AuthorOut:
    data = AuthorOut(
        avatar=obj.avatar,
        ulid=obj.ulid,
        nickname=obj.nickname,
        follower_count=obj.follower_count,
    )
    return data


def convert_channel(obj: ChannelData) -> ChannelOut:
    data = ChannelOut(
        ulid=obj.ulid,
        owner_ulid=obj.owner_ulid,
        avatar=create_url(obj.avatar),
        name=obj.name,
        is_default=obj.is_default,
        description=obj.description,
        count=obj.count,
    )
    return data


def convert_media_user(obj: MediaUserDTO) -> MediaUserOut:
    return MediaUserOut(is_like=obj.is_like, is_subscribe=obj.is_subscribe)


def convert_hashtags(objs: list[HashtagData]) -> list[HashtagOut]:
    return [HashtagOut(ulid=x.ulid, name=x.name) for x in objs]
