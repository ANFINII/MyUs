from ninja import File, Form, Router, UploadedFile
from django.http import JsonResponse

from api.domain.media import MediaDomain
from api.modules.logger import log
from api.models import Music
from api.services.comment import get_comments
from api.services.media import get_musics
from api.services.user import get_user
from api.types.data.common import ErrorData
from api.types.data.media.input import MusicDataIn
from api.types.data.media.index import HashtagData, MusicData, MusicDetailData, MusicDetailOutData, MediaCreateData
from api.utils.enum.index import CommentType
from api.utils.functions.index import create_url
from api.utils.functions.map import comment_type_no_map
from api.utils.functions.user import get_author, get_media_user


class MusicAPI:
    """MusicAPI"""

    router = Router()

    @router.post("", response={201: MediaCreateData, 401: ErrorData})
    def create(request, input: MusicDataIn = Form(...), music: UploadedFile = File(...)):
        """create"""
        log.info("MusicAPI create", input=input, music=music)

        author = get_user(request)
        if not author:
            return 401, ErrorData("Unauthorized")

        obj = MediaDomain.create(model=Music, author=author, music=music, **input.dict())
        data = MediaCreateData(ulid=str(obj.ulid))
        return 201, data

    @router.get("", response={200: list[MusicData]})
    def list(request, search: str | None = None):
        """list"""
        log.info("MusicAPI list", search=search)
        data = get_musics(50, search)
        return 200, data

    @router.get("/{ulid}", response={200: MusicDetailOutData, 404: ErrorData})
    def detail(request, ulid: str, search: str | None = None):
        """detail"""
        log.info("MusicAPI detail", ulid=ulid, search=search)

        obj = MediaDomain.get(model=Music, ulid=ulid, publish=True)
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
