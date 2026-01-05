from django.http import HttpRequest
from ninja import File, Form, Router, UploadedFile

from api.modules.logger import log
from api.src.types.data.comment import CommentData, ReplyData
from api.src.types.data.media import VideoData, MusicData, ComicData, PictureData, BlogData, ChatData, HashtagData
from api.src.types.data.user import AuthorData, MediaUserData
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.comment import CommentOut, ReplyOut
from api.src.types.schema.media import VideoIn, MusicIn, ComicIn, BlogIn, PictureIn, ChatIn
from api.src.types.schema.media import HomeOut, VideoOut, MusicOut, ComicOut, BlogOut, PictureOut, ChatOut, MediaCreateOut, HashtagOut
from api.src.types.schema.media import VideoDetailOut, MusicDetailOut, ComicDetailOut, PictureDetailOut, BlogDetailOut, ChatDetailOut
from api.src.types.schema.media import VideoDetailsOut, MusicDetailsOut, ComicDetailsOut, BlogDetailsOut, PictureDetailsOut, ChatDetailsOut
from api.src.types.schema.message import ChatMessageOut
from api.src.types.schema.user import AuthorOut, MediaUserOut
from api.src.usecase.media import create_video, create_music, create_comic, create_blog, create_picture, create_chat
from api.src.usecase.media import get_home, get_videos, get_musics, get_comics, get_blogs, get_pictures, get_chats
from api.src.usecase.media import get_video_detail, get_music_detail, get_comic_detail, get_blog_detail, get_picture_detail, get_chat_detail
from api.src.usecase.user import get_user


class HomeAPI:
    """HomeAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: HomeOut})
    def get(request: HttpRequest, search: str = ""):
        log.info("HomeAPI get", search=search)

        home = get_home(8, search)
        data = HomeOut(
            videos=[video_out(x) for x in home.videos],
            musics=[music_out(x) for x in home.musics],
            comics=[comic_out(x) for x in home.comics],
            pictures=[picture_out(x) for x in home.pictures],
            blogs=[blog_out(x) for x in home.blogs],
            chats=[chat_out(x) for x in home.chats],
        )

        return 200, data


class VideoAPI:
    """VideoAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 401: ErrorOut})
    def create(
        request: HttpRequest,
        input: VideoIn = Form(...),
        image: UploadedFile = File(...),
        video: UploadedFile = File(...),
        convert: UploadedFile = File(...),
    ):
        log.info("VideoAPI create", input=input, image=image, video=video, convert=convert)

        author = get_user(request)
        if not author:
            return 401, ErrorOut(message="Unauthorized")

        obj = create_video(author=author, image=image, video=video, convert=convert, title=input.title, content=input.content)
        data = MediaCreateOut(ulid=str(obj.ulid))
        return 201, data

    @staticmethod
    @router.get("", response={200: list[VideoOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("VideoAPI list", search=search)
        videos = get_videos(50, search)
        data = [video_out(x) for x in videos]
        return 200, data

    @staticmethod
    @router.get("/{ulid}", response={200: VideoDetailsOut, 404: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("VideoAPI detail", ulid=ulid, search=search)

        obj = get_video_detail(request=request, ulid=ulid, publish=True)
        if obj is None:
            return 404, ErrorOut(message="Not Found")

        objs = get_videos(50, search, obj.id)
        data = VideoDetailsOut(
            detail=VideoDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                image=obj.image,
                video=obj.video,
                convert=obj.convert,
                comments=[comment_out(c) for c in obj.comments],
                hashtags=[hashtag_out(h) for h in obj.hashtags],
                read=obj.read,
                like_count=obj.like_count,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=author_out(obj.author),
                mediaUser=media_user_out(obj.mediaUser),
            ),
            list=[video_out(x) for x in objs],
        )

        return 200, data


class MusicAPI:
    """MusicAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 401: ErrorOut})
    def create(request: HttpRequest, input: MusicIn = Form(...), music: UploadedFile = File(...)):
        log.info("MusicAPI create", input=input, music=music)

        author = get_user(request)
        if not author:
            return 401, ErrorOut(message="Unauthorized")

        obj = create_music(
            author=author,
            music=music,
            title=input.title,
            content=input.content,
            lyric=input.lyric,
            download=input.download,
        )
        data = MediaCreateOut(ulid=str(obj.ulid))
        return 201, data

    @staticmethod
    @router.get("", response={200: list[MusicOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("MusicAPI list", search=search)
        data = get_musics(50, search)
        return 200, [music_out(x) for x in data]

    @staticmethod
    @router.get("/{ulid}", response={200: MusicDetailsOut, 404: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("MusicAPI detail", ulid=ulid, search=search)

        obj = get_music_detail(request=request, ulid=ulid, publish=True)
        if obj is None:
            return 404, ErrorOut(message="Not Found")

        data = MusicDetailsOut(
            detail=MusicDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                lyric=obj.lyric,
                music=obj.music,
                download=obj.download,
                comments=[comment_out(c) for c in obj.comments],
                hashtags=[hashtag_out(h) for h in obj.hashtags],
                read=obj.read,
                like_count=obj.like_count,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=author_out(obj.author),
                mediaUser=media_user_out(obj.mediaUser),
            ),
            list=[music_out(x) for x in get_musics(50, search, obj.id)],
        )

        return 200, data


class ComicAPI:
    """ComicAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 401: ErrorOut})
    def create(request: HttpRequest, input: ComicIn = Form(...), image: UploadedFile = File(...), images: list[UploadedFile] = File(...)):
        log.info("ComicAPI create", input=input, image=image, images=images)

        author = get_user(request)
        if not author:
            return 401, ErrorOut(message="Unauthorized")

        obj = create_comic(author=author, image=image, title=input.title, content=input.content)
        data = MediaCreateOut(ulid=str(obj.ulid))
        return 201, data

    @staticmethod
    @router.get("", response={200: list[ComicOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("ComicAPI list", search=search)
        data = get_comics(50, search)
        return 200, [comic_out(x) for x in data]

    @staticmethod
    @router.get("/{ulid}", response={200: ComicDetailsOut, 404: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("ComicAPI detail", ulid=ulid, search=search)

        obj = get_comic_detail(request=request, ulid=ulid, publish=True)
        if obj is None:
            return 404, ErrorOut(message="Not Found")

        data = ComicDetailsOut(
            detail=ComicDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                image=obj.image,
                comments=[comment_out(c) for c in obj.comments],
                hashtags=[hashtag_out(h) for h in obj.hashtags],
                read=obj.read,
                like_count=obj.like_count,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=author_out(obj.author),
                mediaUser=media_user_out(obj.mediaUser),
            ),
            list=[comic_out(x) for x in get_comics(50, search, obj.id)],
        )

        return 200, data


class PictureAPI:
    """PictureAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 401: ErrorOut})
    def create(request: HttpRequest, input: PictureIn = Form(...), image: UploadedFile = File(...)):
        log.info("PictureAPI create", input=input, image=image)

        author = get_user(request)
        if not author:
            return 401, ErrorOut(message="Unauthorized")

        obj = create_picture(author=author, image=image, title=input.title, content=input.content)
        data = MediaCreateOut(ulid=str(obj.ulid))
        return 201, data

    @staticmethod
    @router.get("", response={200: list[PictureOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("PictureAPI list", search=search)
        data = get_pictures(50, search)
        return 200, [picture_out(x) for x in data]

    @staticmethod
    @router.get("/{ulid}", response={200: PictureDetailsOut, 404: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("PictureAPI detail", ulid=ulid, search=search)

        obj = get_picture_detail(request=request, ulid=ulid, publish=True)
        if obj is None:
            return 404, ErrorOut(message="Not Found")

        data = PictureDetailsOut(
            detail=PictureDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                image=obj.image,
                comments=[comment_out(c) for c in obj.comments],
                hashtags=[hashtag_out(h) for h in obj.hashtags],
                read=obj.read,
                like_count=obj.like_count,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=author_out(obj.author),
                mediaUser=media_user_out(obj.mediaUser),
            ),
            list=[picture_out(x) for x in get_pictures(50, search, obj.id)],
        )

        return 200, data


class BlogAPI:
    """BlogAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 401: ErrorOut})
    def create(request: HttpRequest, input: BlogIn = Form(...), image: UploadedFile = File(...)):
        log.info("BlogAPI create", input=input, image=image)

        author = get_user(request)
        if not author:
            return 401, ErrorOut(message="Unauthorized")

        obj = create_blog(
            author=author,
            image=image,
            title=input.title,
            content=input.content,
            richtext=input.richtext,
        )
        data = MediaCreateOut(ulid=str(obj.ulid))
        return 201, data

    @staticmethod
    @router.get("", response={200: list[BlogOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("BlogAPI list", search=search)
        data = get_blogs(50, search)
        return 200, [blog_out(x) for x in data]

    @staticmethod
    @router.get("/{ulid}", response={200: BlogDetailsOut, 404: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("BlogAPI detail", ulid=ulid, search=search)

        obj = get_blog_detail(request=request, ulid=ulid, publish=True)
        if not obj:
            return 404, ErrorOut(message="Not Found")

        data = BlogDetailsOut(
            detail=BlogDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                richtext=obj.richtext,
                image=obj.image,
                comments=[comment_out(c) for c in obj.comments],
                hashtags=[hashtag_out(h) for h in obj.hashtags],
                read=obj.read,
                like_count=obj.like_count,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=author_out(obj.author),
                mediaUser=media_user_out(obj.mediaUser),
            ),
            list=[blog_out(x) for x in get_blogs(50, search, obj.id)],
        )

        return 200, data


class ChatAPI:
    """ChatAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MediaCreateOut, 401: ErrorOut})
    def create(request: HttpRequest, input: ChatIn = Form(...)):
        log.info("ChatAPI create", input=input)

        author = get_user(request)
        if not author:
            return 401, ErrorOut(message="Unauthorized")

        obj = create_chat(author=author, title=input.title, content=input.content, period=input.period)
        data = MediaCreateOut(ulid=str(obj.ulid))
        return 201, data

    @staticmethod
    @router.get("", response={200: list[ChatOut]})
    def list(request: HttpRequest, search: str = ""):
        log.info("ChatAPI list", search=search)
        data = get_chats(50, search)
        return 200, [chat_out(x) for x in data]

    @staticmethod
    @router.get("/{ulid}", response={200: ChatDetailsOut, 404: ErrorOut})
    def detail(request: HttpRequest, ulid: str, search: str = ""):
        log.info("ChatAPI detail", ulid=ulid, search=search)

        obj = get_chat_detail(request=request, ulid=ulid, publish=True)
        if obj is None:
            return 404, ErrorOut(message="Not Found")

        data = ChatDetailsOut(
            detail=ChatDetailOut(
                ulid=obj.ulid,
                title=obj.title,
                content=obj.content,
                thread=obj.thread,
                joined=obj.joined,
                period=obj.period,
                messages=[ChatMessageOut(ulid=m.ulid, text=m.text, created=m.created, updated=m.updated, author=author_out(m.author)) for m in obj.messages],
                hashtags=[hashtag_out(h) for h in obj.hashtags],
                read=obj.read,
                like_count=obj.like_count,
                publish=obj.publish,
                created=obj.created,
                updated=obj.updated,
                author=author_out(obj.author),
                mediaUser=media_user_out(obj.mediaUser),
            ),
            list=[chat_out(x) for x in get_chats(50, search, obj.id)],
        )

        return 200, data


def author_out(author: AuthorData) -> AuthorOut:
    return AuthorOut(
        avatar=author.avatar,
        ulid=author.ulid,
        nickname=author.nickname,
        follower_count=author.follower_count,
    )


def media_user_out(media_user: MediaUserData) -> MediaUserOut:
    return MediaUserOut(is_like=media_user.is_like, is_follow=media_user.is_follow)


def reply_out(reply: ReplyData) -> ReplyOut:
    return ReplyOut(
        id=reply.id,
        text=reply.text,
        created=reply.created,
        updated=reply.updated,
        is_comment_like=reply.is_comment_like,
        like_count=reply.like_count,
        author=author_out(reply.author),
    )


def comment_out(comment: CommentData) -> CommentOut:
    return CommentOut(
        ulid=comment.ulid,
        text=comment.text,
        created=comment.created,
        updated=comment.updated,
        is_comment_like=comment.is_comment_like,
        like_count=comment.like_count,
        author=author_out(comment.author),
        replys=[reply_out(r) for r in comment.replys],
    )


def hashtag_out(hashtag: HashtagData) -> HashtagOut:
    return HashtagOut(jp_name=hashtag.jp_name)


def video_out(video: VideoData) -> VideoOut:
    return VideoOut(
        ulid=video.ulid,
        title=video.title,
        content=video.content,
        image=video.image,
        video=video.video,
        convert=video.convert,
        comment_count=video.comment_count,
        read=video.read,
        like_count=video.like_count,
        publish=video.publish,
        created=video.created,
        updated=video.updated,
        author=author_out(video.author),
    )


def music_out(music: MusicData) -> MusicOut:
    return MusicOut(
        ulid=music.ulid,
        title=music.title,
        content=music.content,
        lyric=music.lyric,
        music=music.music,
        download=music.download,
        comment_count=music.comment_count,
        read=music.read,
        like_count=music.like_count,
        publish=music.publish,
        created=music.created,
        updated=music.updated,
        author=author_out(music.author),
    )


def comic_out(comic: ComicData) -> ComicOut:
    return ComicOut(
        ulid=comic.ulid,
        title=comic.title,
        content=comic.content,
        image=comic.image,
        comment_count=comic.comment_count,
        read=comic.read,
        like_count=comic.like_count,
        publish=comic.publish,
        created=comic.created,
        updated=comic.updated,
        author=author_out(comic.author),
    )


def blog_out(blog: BlogData) -> BlogOut:
    return BlogOut(
        ulid=blog.ulid,
        title=blog.title,
        content=blog.content,
        image=blog.image,
        comment_count=blog.comment_count,
        read=blog.read,
        like_count=blog.like_count,
        publish=blog.publish,
        created=blog.created,
        updated=blog.updated,
        author=author_out(blog.author),
    )


def picture_out(picture: PictureData) -> PictureOut:
    return PictureOut(
        ulid=picture.ulid,
        title=picture.title,
        content=picture.content,
        image=picture.image,
        comment_count=picture.comment_count,
        read=picture.read,
        like_count=picture.like_count,
        publish=picture.publish,
        created=picture.created,
        updated=picture.updated,
        author=author_out(picture.author),
    )


def chat_out(chat: ChatData) -> ChatOut:
    return ChatOut(
        ulid=chat.ulid,
        title=chat.title,
        content=chat.content,
        thread=chat.thread,
        joined=chat.joined,
        period=chat.period,
        read=chat.read,
        like_count=chat.like_count,
        publish=chat.publish,
        created=chat.created,
        updated=chat.updated,
        author=author_out(chat.author),
    )
