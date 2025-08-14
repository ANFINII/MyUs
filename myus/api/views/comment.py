from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from api.types.data.comment import CommentInData
from api.domain.comment import CommentDomain
from api.services.comment import create_comment, get_comments
from api.services.user import get_user
from api.utils.enum.response import ApiResponse
from api.utils.functions.response import DataResponse


class CommentAPI(APIView):
    def get(self, request) -> DataResponse:
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        data = request.data
        comments = get_comments(type_no=data["type_no"], object_id=data["object_id"], user_id=user.id)
        return DataResponse(comments, HTTP_200_OK)

    def post(self, request) -> DataResponse:
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        data = request.data

        comment_data = CommentInData(
            author=user,
            text=data["text"],
            type_no=data["type_no"],
            type_name=data["type_name"],
            object_id=data["object_id"],
            parent_id=data.get("parent_id", None),
        )

        data = create_comment(comment_data)
        return DataResponse(data, HTTP_201_CREATED)

    def put(self, request, id: int) -> DataResponse:
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        data = request.data
        comment = CommentDomain.get(id)
        if not comment:
            return ApiResponse.NOT_FOUND.run()

        CommentDomain.update(comment, text=data["text"])
        return DataResponse(None, HTTP_200_OK)

    def delete(self, request, id: int) -> DataResponse:
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()

        comment = CommentDomain.get(id)
        if not comment:
            return ApiResponse.NOT_FOUND.run()

        CommentDomain.update(comment, deleted=True)
        return DataResponse(None, HTTP_200_OK)
