from apps.api.types.comment import Comment
from apps.api.utils.functions.user import get_author


def get_comment(comment: Comment) -> dict:
    data = {
        'id': comment.id,
        'text': comment.text,
        'reply_count': comment.reply_count,
        'created': comment.created,
        'author': get_author(comment.author),
    }
    return data
