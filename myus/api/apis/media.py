from ninja import File, Form, Router, UploadedFile
from api.domain.media import MediaDomain
from api.modules.logger import log
from api.models.media import Video, Music, Comic, Picture, Blog, Chat
from api.services.comment import get_comments
from api.services.message import get_messages
from api.services.media import get_home, get_videos,get_musics, get_comics, get_pictures, get_blogs, get_chats
from api.services.user import get_user
from api.types.data.common import ErrorData
from api.types.data.media.index import HomeData, HashtagData, MediaCreateData
from api.types.data.media.index import VideoData, VideoDetailData
from api.types.data.media.index import MusicData, MusicDetailData
from api.types.data.media.index import ComicData, ComicDetailData
from api.types.data.media.index import PictureData, PictureDetailData
from api.types.data.media.index import BlogData, BlogDetailData
from api.types.data.media.index import ChatData, ChatDetailData
from api.types.data.media.input import VideoInData, MusicInData, ComicInData, PictureInData, BlogInData, ChatInData
from api.types.data.media.output import VideoDetailOutData, MusicDetailOutData, ComicDetailOutData, PictureDetailOutData, BlogDetailOutData, ChatDetailOutData
from api.utils.enum.index import CommentType
from api.utils.functions.index import create_url
from api.utils.functions.map import comment_type_no_map
from api.utils.functions.user import get_author, get_media_user


class HomeAPI:
    """HomeAPI"""

    router = Router()

    @router.get("", response={200: HomeData})
    def get(request, search: str | None = None):
        log.info("HomeAPI get", search=search)

        data = get_home(8, search)
        return 200, data


class VideoAPI:
    """VideoAPI"""

    router = Router()

    @router.post("", response={201: MediaCreateData, 401: ErrorData})
    def create(
        request,
        input: VideoInData = Form(...),
        image: UploadedFile = File(...),
        video: UploadedFile = File(...),
        convert: UploadedFile = File(...),
    ):
        log.info("VideoAPI create", input=input, image=image, video=video, convert=convert)

        author = get_user(request)
        if not author:
            return 401, ErrorData("Unauthorized")

        obj = MediaDomain.create(model=Video(), author=author, video=video, **input.dict())
        data = MediaCreateData(ulid=str(obj.ulid))
        return 201, data

    @router.get("", response={200: list[VideoData]})
    def list(request, search: str | None):
        log.info("VideoAPI list", search=search)
        data = get_videos(50, search)
        return 200, data

    @router.get("/{ulid}", response={200: VideoDetailOutData, 404: ErrorData})
    def detail(request, ulid: str, search: str | None):
        log.info("VideoAPI detail", ulid=ulid, search=search)

        obj = MediaDomain.get(model=Video(), ulid=ulid, publish=True)
        if not obj:
            return 404, ErrorData("Not Found")

        user = get_user(request)
        user_id = user.id if user else None
        type_no = comment_type_no_map(CommentType.VIDEO)
        comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)

        data = VideoDetailOutData(
            detail=VideoDetailData(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                image=create_url(obj.image.url),
                video=create_url(obj.video.url),
                convert=create_url(obj.convert.url),
                comments=comments,
                hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
                read=obj.read,
                like_count=obj.total_like(),
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=get_author(obj.author),
                mediaUser=get_media_user(obj, user),
            ),
            list=get_videos(50, search, obj.id),
        )

        return 200, data


class MusicAPI:
    """MusicAPI"""

    router = Router()

    @router.post("", response={201: MediaCreateData, 401: ErrorData})
    def create(request, input: MusicInData = Form(...), music: UploadedFile = File(...)):
        log.info("MusicAPI create", input=input, music=music)

        author = get_user(request)
        if not author:
            return 401, ErrorData("Unauthorized")

        obj = MediaDomain.create(model=Music(), author=author, music=music, **input.dict())
        data = MediaCreateData(ulid=str(obj.ulid))
        return 201, data

    @router.get("", response={200: list[MusicData]})
    def list(request, search: str | None):
        log.info("MusicAPI list", search=search)
        data = get_musics(50, search)
        return 200, data

    @router.get("/{ulid}", response={200: MusicDetailOutData, 404: ErrorData})
    def detail(request, ulid: str, search: str | None):
        log.info("MusicAPI detail", ulid=ulid, search=search)

        obj = MediaDomain.get(model=Music(), ulid=ulid, publish=True)
        if not obj:
            return 404, ErrorData("Not Found")

        user = get_user(request)
        user_id = user.id if user else None
        type_no = comment_type_no_map(CommentType.MUSIC)
        comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)

        data = MusicDetailOutData(
            detail=MusicDetailData(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                lyric=obj.lyric,
                music=create_url(obj.music.url),
                download=obj.download,
                comments=comments,
                hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
                read=obj.read,
                like_count=obj.total_like(),
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=get_author(obj.author),
                mediaUser=get_media_user(obj, user),
            ),
            list=get_musics(50, search, obj.id),
        )

        return 200, data


class ComicAPI:
    """ComicAPI"""

    router = Router()

    @router.post("", response={201: MediaCreateData, 401: ErrorData})
    def create(request, input: ComicInData = Form(...), image: UploadedFile = File(...), images: list[UploadedFile] = File(...)):
        log.info("ComicAPI create", input=input, image=image, images=images)

        author = get_user(request)
        if not author:
            return 401, ErrorData("Unauthorized")

        obj = MediaDomain.create(model=Comic(), author=author, image=image, **input.dict())
        data = MediaCreateData(ulid=str(obj.ulid))
        return 201, data

    @router.get("", response={200: list[ComicData]})
    def list(request, search: str | None):
        log.info("ComicAPI list", search=search)
        data = get_comics(50, search)
        return 200, data

    @router.get("/{ulid}", response={200: ComicDetailOutData, 404: ErrorData})
    def detail(request, ulid: str, search: str | None):
        log.info("ComicAPI detail", ulid=ulid, search=search)

        obj = MediaDomain.get(model=Comic(), ulid=ulid, publish=True)
        if not obj:
            return 404, ErrorData("Not Found")

        user = get_user(request)
        user_id = user.id if user else None
        type_no = comment_type_no_map(CommentType.COMIC)
        comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)

        data = ComicDetailOutData(
            detail=ComicDetailData(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                image=create_url(obj.image.url),
                comments=comments,
                hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
                read=obj.read,
                like_count=obj.total_like(),
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=get_author(obj.author),
                mediaUser=get_media_user(obj, user),
            ),
            list=get_comics(50, search, obj.id),
        )

        return 200, data


class PictureAPI:
    """PictureAPI"""

    router = Router()

    @router.post("", response={201: MediaCreateData, 401: ErrorData})
    def create(request, input: PictureInData = Form(...), image: UploadedFile = File(...)):
        log.info("PictureAPI create", input=input, image=image)

        author = get_user(request)
        if not author:
            return 401, ErrorData("Unauthorized")

        obj = MediaDomain.create(model=Picture(), author=author, image=image, **input.dict())
        data = MediaCreateData(ulid=str(obj.ulid))
        return 201, data

    @router.get("", response={200: list[PictureData]})
    def list(request, search: str | None):
        log.info("PictureAPI list", search=search)
        data = get_pictures(50, search)
        return 200, data

    @router.get("/{ulid}", response={200: PictureDetailOutData, 404: ErrorData})
    def detail(request, ulid: str, search: str | None):
        log.info("PictureAPI detail", ulid=ulid, search=search)

        obj = MediaDomain.get(model=Picture(), ulid=ulid, publish=True)
        if not obj:
            return 404, ErrorData("Not Found")

        user = get_user(request)
        user_id = user.id if user else None
        type_no = comment_type_no_map(CommentType.PICTURE)
        comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)

        data = PictureDetailOutData(
            detail=PictureDetailData(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                image=create_url(obj.image.url),
                comments=comments,
                hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
                read=obj.read,
                like_count=obj.total_like(),
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=get_author(obj.author),
                mediaUser=get_media_user(obj, user),
            ),
            list=get_pictures(50, search, obj.id),
        )

        return 200, data


class BlogAPI:
    """BlogAPI"""

    router = Router()

    @router.post("", response={201: MediaCreateData, 401: ErrorData})
    def create(request, input: BlogInData = Form(...), image: UploadedFile = File(...)):
        log.info("BlogAPI create", input=input, image=image)

        author = get_user(request)
        if not author:
            return 401, ErrorData("Unauthorized")

        obj = MediaDomain.create(model=Blog(), author=author, image=image, **input.dict())
        data = MediaCreateData(ulid=str(obj.ulid))
        return 201, data

    @router.get("", response={200: list[BlogData]})
    def list(request, search: str | None):
        log.info("BlogAPI list", search=search)
        data = get_blogs(50, search)
        return 200, data

    @router.get("/{ulid}", response={200: BlogDetailOutData, 404: ErrorData})
    def detail(request, ulid: str, search: str | None):
        log.info("BlogAPI detail", ulid=ulid, search=search)

        obj = MediaDomain.get(model=Blog(), ulid=ulid, publish=True)
        if not obj:
            return 404, ErrorData("Not Found")

        user = get_user(request)
        user_id = user.id if user else None
        type_no = comment_type_no_map(CommentType.BLOG)
        comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)

        data = BlogDetailOutData(
            detail=BlogDetailData(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                richtext=obj.richtext,
                image=create_url(obj.image.url),
                comments=comments,
                hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
                read=obj.read,
                like_count=obj.total_like(),
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=get_author(obj.author),
                mediaUser=get_media_user(obj, user),
            ),
            list=get_blogs(50, search, obj.id),
        )

        return 200, data


class ChatAPI:
    """ChatAPI"""

    router = Router()

    @router.post("", response={201: MediaCreateData, 401: ErrorData})
    def create(request, input: ChatInData = Form(...)):
        log.info("ChatAPI create", input=input)

        author = get_user(request)
        if not author:
            return 401, ErrorData("Unauthorized")

        obj = MediaDomain.create(model=Chat(), author=author, **input.dict())
        data = MediaCreateData(ulid=str(obj.ulid))
        return 201, data

    @router.get("", response={200: list[ChatData]})
    def list(request, search: str | None):
        log.info("ChatAPI list", search=search)
        data = get_chats(50, search)
        return 200, data

    @router.get("/{ulid}", response={200: ChatDetailOutData, 404: ErrorData})
    def detail(request, ulid: str, search: str | None):
        log.info("ChatAPI detail", ulid=ulid, search=search)

        obj = MediaDomain.get(model=Chat(), ulid=ulid, publish=True)
        if not obj:
            return 404, ErrorData("Not Found")

        user = get_user(request)
        messages = get_messages(chat_id=obj.id)

        data = ChatDetailOutData(
            detail=ChatDetailData(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                messages=messages,
                hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
                read=obj.read,
                like_count=obj.total_like(),
                thread=obj.thread_count(),
                joined=obj.joined_count(),
                period=obj.period,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=get_author(obj.author),
                mediaUser=get_media_user(obj, user),
            ),
            list=get_chats(50, search, obj.id),
        )

        return 200, data
