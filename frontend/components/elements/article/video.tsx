import Link from 'next/link'
import AuthorSpace from 'components/elements/common/author_space'
import ContentTitle from 'components/elements/common/content_title'
import { VideoType } from 'lib/utils/type'


export default function PictureArticle({ datas }: { datas: any }) {
  return (
    <article className="article_list">
      {datas.video.map((data: VideoType) => {
        const image_url = process.env.NEXT_PUBLIC_API_URL + data.image
        const convert_url = process.env.NEXT_PUBLIC_API_URL + data.convert
        return (
          <section className="section_list" key={data.id}>
            <div className="main_decolation">
              <div className="video video_auto">
                <Link href={`/video/${data.id}`}>
                  <a>
                    <video className="video-js vjs-16-9" muted width="272" height="153" controlsList="nodownload" poster={ image_url } data-setup="">
                      {/* onContextMenu="return false" */}
                      <source src={ convert_url } type="video/mp4" data-label="360p" data-res="360" />
                      <p>動画を再生するには、videoタグをサポートしたブラウザが必要です!</p>
                      <track kind="captions" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
                      <track kind="subtitles" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
                    </video>
                  </a>
                </Link>
                <Link href={`/video/${data.id}`}>
                  <a className="author_space">
                    <AuthorSpace author={data.author} />
                    <ContentTitle data={data} />
                  </a>
                </Link>
              </div>
            </div>
          </section>
        )
      })}
    </article>
  )
}
