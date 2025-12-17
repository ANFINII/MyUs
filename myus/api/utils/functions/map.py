from api.utils.enum.index import CommentTypeNo, CommentType, MediaType


def comment_type_map(type_no: CommentTypeNo) -> CommentType:
    return CommentType[type_no.name]


def comment_type_no_map(type_name: CommentType) -> CommentTypeNo:
    return CommentTypeNo[type_name.name]
