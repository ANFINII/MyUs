import Link from 'next/link'
import config from 'api/config'
import { Video } from 'types/media'
import AuthorSpace from 'components/widgets/Common/AuthorSpace'
import ContentTitle from 'components/widgets/Common/ContentTitle'

interface Props {
  data: Video
}

export default function ArticleVideo(props: Props) {
  const { data } = props

  const pictureUrl = config.baseUrl + data.image
  const convertUrl = config.baseUrl + data.convert
  const imageUrl = config.baseUrl + data.author.image
  const nickname = data.author.nickname

  return (
    <section className="section_list">
      <div className="main_decolation">
        <div className="video video_auto">
          <Link href={`/media/video/${data.id}`}>
            <video className="video-js" muted width={272} height={153} controlsList="nodownload" poster={pictureUrl} data-setup="">
              {/* onContextMenu="return false" */}
              <source src={convertUrl} type="video/mp4" data-label="360p" data-res="360" />
              <p>動画を再生するには、videoタグをサポートしたブラウザが必要です!</p>
              <track kind="captions" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
              <track kind="subtitles" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
            </video>
            <div className="author_space">
              <AuthorSpace imageUrl={imageUrl} nickname={nickname} />
              <ContentTitle title={data.title} nickname={nickname} read={data.read} totalLike={data.like} created={data.created} />
            </div>
          </Link>
        </div>
      </div>
    </section>
  )
}
