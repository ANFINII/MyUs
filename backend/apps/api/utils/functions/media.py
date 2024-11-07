from apps.api.types.data.media import HashtagData
from apps.myus.models.media import HashTag
from apps.api.types.data.media import VideoDetailData
from apps.myus.models.media import Video
from apps.myus.models.comment import Comment
from apps.api.utils.functions.comment import get_comment_data
from apps.api.utils.functions.user import get_author


def get_hashtag(hashtag: HashTag) -> HashtagData:
    return HashtagData(jp_name=hashtag.jp_name)


def get_video_detail_data(video: Video, comments: list[Comment]) -> HashtagData:
    data = VideoDetailData(
            id=video.id,
            title=video.title,
            content=video.content,
            image=video.image.url,
            video=video.video.url,
            convert=video.convert.url,
            comments=[get_comment_data(comment) for comment in comments],
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
