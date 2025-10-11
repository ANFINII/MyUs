from api.models.media import HashTag, Video
from api.types.data.comment import CommentData
from api.types.data.media.index import HashtagData, VideoDetailData
from api.utils.functions.user import get_author
from api.utils.functions.index import create_url


def get_hashtag(hashtag: HashTag) -> HashtagData:
    return HashtagData(jp_name=hashtag.jp_name)


def get_video_detail_data(video: Video, comments: list[CommentData]) -> VideoDetailData:
    data = VideoDetailData(
        id=video.id,
        title=video.title,
        content=video.content,
        image=create_url(video.image.url),
        video=create_url(video.video.url),
        convert=create_url(video.convert.url),
        comments=comments,
        hashtags=[get_hashtag(hashtag) for hashtag in video.hashtag.all()],
        like=video.total_like(),
        read=video.read,
        comment_count=video.comment_count(),
        publish=video.publish,
        created=video.created,
        updated=video.updated,
        author=get_author(video.author),
    )
    return data
