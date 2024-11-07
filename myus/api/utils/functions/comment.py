from django.db.models import Exists, OuterRef
from apps.myus.models.comment import Comment
from apps.api.types.data.comment import CommentData
from apps.api.utils.functions.user import get_author


def get_comments(obj) -> Comment:
    filter_kwargs = {'id': OuterRef('pk'), 'like': obj.author.id}
    subquery = obj.comment.filter(**filter_kwargs)
    comments = obj.comment.filter(parent__isnull=True).annotate(is_comment_like=Exists(subquery))
    return comments


def get_comment_data(comment: Comment) -> CommentData:
    data = CommentData(
        id=comment.id,
        text=comment.text,
        reply_count=comment.reply_count,
        created=comment.created,
        author=get_author(comment.author),
    )
    return data
