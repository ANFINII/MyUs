from django.http import HttpRequest
from ninja import File, Form, Router, UploadedFile
from api.modules.logger import log
from api.src.types.data.comment import CommentGetData, ReplyData
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.comic.data import ComicData
from api.src.domain.interface.media.picture.data import PictureData
from api.src.domain.interface.media.blog.data import BlogData
from api.src.domain.interface.media.chat.data import ChatData
from api.src.domain.interface.media.data import HashtagData
from api.src.domain.interface.channel.data import ChannelData
from api.utils.functions.index import create_url
from api.src.types.data.message import MessageData
from api.src.types.data.user import AuthorData, MediaUserData
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.comment import CommentOut, ReplyOut
from api.src.types.schema.media import VideoIn, MusicIn, ComicIn,PictureIn, BlogIn, ChatIn
from api.src.types.schema.media import HomeOut, VideoOut, MusicOut, ComicOut, PictureOut, BlogOut, ChatOut, MediaCreateOut, HashtagOut
from api.src.types.schema.media import VideoDetailOut, MusicDetailOut, ComicDetailOut, PictureDetailOut, BlogDetailOut, ChatDetailOut
from api.src.types.schema.media import VideoDetailsOut, MusicDetailsOut, ComicDetailsOut, PictureDetailsOut, BlogDetailsOut, ChatDetailsOut
from api.src.types.schema.message import ChatMessageOut
from api.src.types.schema.channel import ChannelOut
from api.src.types.schema.user import AuthorOut, MediaUserOut
from api.src.usecase.auth import auth_check
from api.src.usecase.channel import get_channel
from api.src.usecase.media import create_video, create_music, create_comic, create_blog, create_picture, create_chat
from api.src.usecase.media import get_home, get_videos, get_musics, get_comics, get_blogs, get_pictures, get_chats
from api.src.usecase.media import get_video_detail, get_music_detail, get_comic_detail, get_blog_detail, get_picture_detail, get_chat_detail


class HomeAPI:
    """HomeAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: HomeOut})
    def get(request: HttpRequest, search: str = ""):
        log.info("HomeAPI get", search=search)

        home = get_home(8, search)
        data = HomeOut(
            videos=convert_videos(home.videos),
            musics=convert_musics(home.musics),
            comics=convert_comics(home.comics),
            pictures=convert_pictures(home.pictures),
            blogs=convert_blogs(home.blogs),
            chats=convert_chats(home.chats),
        )

        return 200, data


class VideoAPI:
    """VideoAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 400: ErrorOut, 401: ErrorOut})
    def create(
        request: HttpRequest,
        input: VideoIn = Form(...),
        image: UploadedFile = File(...),
        video: UploadedFile = File(...),
        convert: UploadedFile = File(...),
    ):
        log.info("VideoAPI create", input=input, image=image, video=video, convert=convert)

        if auth_check(request) is None:
            return 401, ErrorOut(message="Unauthorized")

        channel = get_channel(input.channel_ulid)
        if channel is None:
            return 400, ErrorOut(message="チャンネルが見つかりません")

        obj = create_video(channel=channel, input=input, image=image, video=video, convert=convert)
        data = MediaCreateOut(ulid=obj.ulid)
        return 201, data

    @staticmethod
    @router.get("", response={200: list[VideoOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("VideoAPI list", search=search)
        objs = get_videos(50, search)
        data = convert_videos(objs)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: VideoDetailsOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("VideoAPI detail", ulid=ulid, search=search)

        user_id = auth_check(request)
        obj = get_video_detail(user_id=user_id, ulid=ulid, publish=True)
        objs = get_videos(50, search, obj.id)

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
    @router.post("", response={201: MediaCreateOut, 400: ErrorOut, 401: ErrorOut})
    def create(request: HttpRequest, input: MusicIn = Form(...), music: UploadedFile = File(...)):
        log.info("MusicAPI create", input=input, music=music)

        if auth_check(request) is None:
            return 401, ErrorOut(message="Unauthorized")

        channel = get_channel(input.channel_ulid)
        if channel is None:
            return 400, ErrorOut(message="チャンネルが見つかりません")

        obj = create_music(channel=channel, input=input, music=music)
        data = MediaCreateOut(ulid=obj.ulid)
        return 201, data

    @staticmethod
    @router.get("", response={200: list[MusicOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("MusicAPI list", search=search)
        objs = get_musics(50, search)
        data = convert_musics(objs)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: MusicDetailsOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("MusicAPI detail", ulid=ulid, search=search)

        user_id = auth_check(request)
        obj = get_music_detail(user_id=user_id, ulid=ulid, publish=True)
        objs = get_musics(50, search, obj.id)

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


class ComicAPI:
    """ComicAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 400: ErrorOut, 401: ErrorOut})
    def create(request: HttpRequest, input: ComicIn = Form(...), image: UploadedFile = File(...), images: list[UploadedFile] = File(...)):
        log.info("ComicAPI create", input=input, image=image, images=images)

        if auth_check(request) is None:
            return 401, ErrorOut(message="Unauthorized")

        channel = get_channel(input.channel_ulid)
        if channel is None:
            return 400, ErrorOut(message="チャンネルが見つかりません")

        obj = create_comic(channel=channel, input=input, image=image)
        data = MediaCreateOut(ulid=obj.ulid)
        return 201, data

    @staticmethod
    @router.get("", response={200: list[ComicOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("ComicAPI list", search=search)
        objs = get_comics(50, search)
        data = convert_comics(objs)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: ComicDetailsOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("ComicAPI detail", ulid=ulid, search=search)

        user_id = auth_check(request)
        obj = get_comic_detail(user_id=user_id, ulid=ulid, publish=True)
        objs = get_comics(50, search, obj.id)

        data = ComicDetailsOut(
            detail=ComicDetailOut(
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
            list=convert_comics(objs),
        )

        return 200, data


class PictureAPI:
    """PictureAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 400: ErrorOut, 401: ErrorOut})
    def create(request: HttpRequest, input: PictureIn = Form(...), image: UploadedFile = File(...)):
        log.info("PictureAPI create", input=input, image=image)

        if auth_check(request) is None:
            return 401, ErrorOut(message="Unauthorized")

        channel = get_channel(input.channel_ulid)
        if channel is None:
            return 400, ErrorOut(message="チャンネルが見つかりません")

        obj = create_picture(channel=channel, input=input, image=image)
        data = MediaCreateOut(ulid=obj.ulid)
        return 201, data

    @staticmethod
    @router.get("", response={200: list[PictureOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("PictureAPI list", search=search)
        objs = get_pictures(50, search)
        data = convert_pictures(objs)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: PictureDetailsOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("PictureAPI detail", ulid=ulid, search=search)

        user_id = auth_check(request)
        obj = get_picture_detail(user_id=user_id, ulid=ulid, publish=True)
        objs = get_pictures(50, search, obj.id)

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


class BlogAPI:
    """BlogAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 400: ErrorOut, 401: ErrorOut})
    def create(request: HttpRequest, input: BlogIn = Form(...), image: UploadedFile = File(...)):
        log.info("BlogAPI create", input=input, image=image)

        if auth_check(request) is None:
            return 401, ErrorOut(message="Unauthorized")

        channel = get_channel(input.channel_ulid)
        if channel is None:
            return 400, ErrorOut(message="チャンネルが見つかりません")

        obj = create_blog(channel=channel, input=input, image=image)
        data = MediaCreateOut(ulid=obj.ulid)
        return 201, data

    @staticmethod
    @router.get("", response={200: list[BlogOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("BlogAPI list", search=search)
        objs = get_blogs(50, search)
        data = convert_blogs(objs)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: BlogDetailsOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("BlogAPI detail", ulid=ulid, search=search)

        user_id = auth_check(request)
        obj = get_blog_detail(user_id=user_id, ulid=ulid, publish=True)
        objs = get_blogs(50, search, obj.id)

        data = BlogDetailsOut(
            detail=BlogDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                richtext=obj.richtext,
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


class ChatAPI:
    """ChatAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 400: ErrorOut, 401: ErrorOut})
    def create(request: HttpRequest, input: ChatIn = Form(...)):
        log.info("ChatAPI create", input=input)

        if auth_check(request) is None:
            return 401, ErrorOut(message="Unauthorized")

        channel = get_channel(input.channel_ulid)
        if channel is None:
            return 400, ErrorOut(message="チャンネルが見つかりません")

        obj = create_chat(channel=channel, input=input)
        data = MediaCreateOut(ulid=obj.ulid)
        return 201, data

    @staticmethod
    @router.get("", response={200: list[ChatOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("ChatAPI list", search=search)
        objs = get_chats(50, search)
        data = convert_chats(objs)
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: ChatDetailsOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("ChatAPI detail", ulid=ulid, search=search)

        user_id = auth_check(request)
        obj = get_chat_detail(user_id=user_id, ulid=ulid, publish=True)
        objs = get_chats(50, search, obj.id)

        data = ChatDetailsOut(
            detail=ChatDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                thread=obj.thread,
                joined=obj.joined,
                period=obj.period,
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


def convert_videos(objs: list[VideoData]) -> list[VideoOut]:
    data = [
        VideoOut(
            ulid=x.ulid,
            title=x.title,
            content=x.content,
            image=x.image,
            video=x.video,
            convert=x.convert,
            comment_count=x.comment_count,
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
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
            comment_count=x.comment_count,
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
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
            comment_count=x.comment_count,
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
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
            comment_count=x.comment_count,
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
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
            comment_count=x.comment_count,
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
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
            period=x.period,
            read=x.read,
            like=x.like,
            publish=x.publish,
            created=x.created,
            updated=x.updated,
            channel=convert_channel(x.channel),
        ) for x in objs
    ]
    return data


def convert_comments(objs: list[CommentGetData]) -> list[CommentOut]:
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


def convert_replys(objs: list[ReplyData]) -> list[ReplyOut]:
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


def convert_messages(objs: list[MessageData]) -> list[ChatMessageOut]:
    data = [
        ChatMessageOut(
            ulid=m.ulid,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=convert_author(m.author),
        ) for m in objs
    ]
    return data


def convert_author(obj: AuthorData) -> AuthorOut:
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
        avatar=create_url(obj.avatar),
        name=obj.name,
        is_default=obj.is_default,
        description=obj.description,
    )
    return data


def convert_media_user(obj: MediaUserData) -> MediaUserOut:
    return MediaUserOut(is_like=obj.is_like, is_subscribe=obj.is_subscribe)


def convert_hashtags(objs: list[HashtagData]) -> list[HashtagOut]:
    return [HashtagOut(jp_name=x.jp_name) for x in objs]
