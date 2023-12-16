import Link from 'next/link'
import { Video } from 'types/internal/media'
import AuthorSpace from 'components/widgets/Common/AuthorSpace'
import ContentTitle from 'components/widgets/Common/ContentTitle'

interface Props {
  data: Video
}

export default function ArticleVideo(props: Props) {
  const { data } = props
  const { image, convert, title, read, like, created, author } = data

  return (
    <section className="section_list">
      <div className="main_decolation">
        <div className="video video_auto">
          <Link href={`/media/video/${data.id}`}>
            <video className="video-js" muted width={272} height={153} controlsList="nodownload" poster={image} data-setup="">
              {/* onContextMenu="return false" */}
              <source src={convert} type="video/mp4" data-label="360p" data-res="360" />
              <p>動画を再生するには、videoタグをサポートしたブラウザが必要です!</p>
              <track kind="captions" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
              <track kind="subtitles" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
            </video>
            <div className="author_space">
              <AuthorSpace imageUrl={author.image} nickname={author.nickname} />
              <ContentTitle title={title} nickname={author.nickname} read={read} totalLike={like} created={created} />
            </div>
          </Link>
        </div>
      </div>
    </section>
  )
}
