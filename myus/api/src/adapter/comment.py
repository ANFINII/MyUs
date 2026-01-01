from ninja import Router
from api.modules.logger import log
from api.src.domain.media.blog import BlogDomain
from api.src.domain.comment import CommentDomain
from api.src.usecase.comment import create_comment, get_comments
from api.src.usecase.user import get_user
from api.src.types.data.auth import MessageData
from api.src.types.data.comment.index import CommentData, CommentCreateData
from api.src.types.data.comment.input import CommentListInData, CommentCreateInData, CommentUpdateInData
from api.src.types.data.common import ErrorData
from api.utils.functions.user import get_author


class CommentAPI:
    """コメントAPI"""

    router = Router()

    @router.get("", response={200: list[CommentData], 401: ErrorData})
    def get(request, query: CommentListInData):
        log.info("CommentAPI get", type_no=query.type_no, object_id=query.object_id)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        data = get_comments(
            type_no=query.type_no,
            object_id=query.object_id,
            user_id=user.id
        )
        return 200, data

    @router.post("", response={201: CommentData, 400: MessageData, 401: ErrorData})
    def post(request, input: CommentCreateInData):
        log.info("CommentAPI post", input=input)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        obj = BlogDomain.get(ulid=input.object_ulid, publish=True)
        if not obj:
            return 400, MessageData(error=True, message="対象メディアが見つかりません")

        comment = CommentDomain.get(input.parent_ulid) if input.parent_ulid else None
        parent_id = comment.id if comment else None

        comment_data = CommentCreateData(
            author=get_author(user),
            text=input.text,
            type_no=input.type_no,
            type_name=input.type_name,
            object_id=obj.id,
            parent_id=parent_id,
        )

        try:
            data = create_comment(comment_data)
            return 201, data
        except Exception as e:
            log.error("CommentAPI post error", exc=e)
            return 400, MessageData(error=True, message="コメントの作成に失敗しました")

    @router.put("/{comment_ulid}", response={200: MessageData, 400: MessageData, 401: ErrorData, 404: ErrorData})
    def put(request, comment_ulid: str, input: CommentUpdateInData):
        log.info("CommentAPI put", comment_ulid=comment_ulid, input=input)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        comment = CommentDomain.get(comment_ulid)
        if not comment:
            return 404, ErrorData(message="コメントが見つかりません")

        try:
            CommentDomain.update(comment, text=input.text)
            return 200, MessageData(error=False, message="コメントを更新しました")
        except Exception as e:
            log.error("CommentAPI put error", exc=e)
            return 400, MessageData(error=True, message="コメントの更新に失敗しました")

    @router.delete("/{comment_ulid}", response={200: MessageData, 400: MessageData, 401: ErrorData, 404: ErrorData})
    def delete(request, comment_ulid: str):
        log.info("CommentAPI delete", comment_ulid=comment_ulid)

        user = get_user(request)
        if not user:
            return 401, ErrorData(message="Unauthorized")

        comment = CommentDomain.get(comment_ulid)
        if not comment:
            return 404, ErrorData(message="コメントが見つかりません")

        try:
            CommentDomain.update(comment, deleted=True)
            return 200, MessageData(error=False, message="コメントを削除しました")
        except Exception as e:
            log.error("CommentAPI delete error", exc=e)
            return 400, MessageData(error=True, message="コメントの削除に失敗しました")
