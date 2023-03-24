import Link from 'next/link'
import {VideoResponse} from 'utils/type'
import config from 'api/config'
import AuthorSpace from 'components/elements/Common/AuthorSpace'
import ContentTitle from 'components/elements/Common/ContentTitle'

interface Props {datas: Array<VideoResponse>}

export default function ArticleVideo(props: Props) {
  const {datas} = props
  return (
    <article className="article_list">
      {datas.map((data) => {
        const pictureUrl = config.baseUrl + data.image
        const convertUrl = config.baseUrl + data.convert
        const imageUrl = config.baseUrl + data.author.image
        const nickname = data.author.nickname
        return (
          <section className="section_list" key={data.id}>
            <div className="main_decolation">
              <div className="video video_auto">
                <Link href={`/video/${data.id}`}>
                  <video className="video-js" muted width={272} height={153} controlsList="nodownload" poster={pictureUrl} data-setup="">
                    {/* onContextMenu="return false" */}
                    <source src={convertUrl} type="video/mp4" data-label="360p" data-res="360" />
                    <p>動画を再生するには、videoタグをサポートしたブラウザが必要です!</p>
                    <track kind="captions" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
                    <track kind="subtitles" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
                  </video>
                </Link>
                <Link href={`/video/${data.id}`} className="author_space">
                  <AuthorSpace imageUrl={imageUrl} nickname={nickname} />
                  <ContentTitle title={data.title} nickname={nickname} read={data.read} totalLike={data.like} created={data.created} />
                </Link>
              </div>
            </div>
          </section>
        )
      })}
    </article>
  )
}