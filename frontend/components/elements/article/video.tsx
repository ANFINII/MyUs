import Link from 'next/link'
import AuthorSpace from 'components/elements/common/author_space'
import ContentTitle from 'components/elements/common/content_title'
import { VideoType } from 'lib/utils/type'

export default function PictureArticle({ datas }: { datas: any }) {
  return (
    <article className="article_list">
      {datas.data.map((data: VideoType) => {
        return(
          <section className="section_list" key={data.id}>
            <div className="main_decolation">
              <div className="video video_auto">
                <Link href={`/video/${data.id}`}>
                  <a>
                    <video className="video-js vjs-16-9" muted width="272" height="153" controlsList="nodownload"
                      // onContextMenu={'return': false}
                      poster={data.image} data-setup="">
                      <source src="" type="video/mp4" data-label="360p" data-res="360" />
                      <p>動画を再生するには、videoタグをサポートしたブラウザが必要です!</p>
                      <track kind="captions" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
                      <track kind="subtitles" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
                    </video>
                  </a>
                </Link>
                <Link href={`/video/${data.id}`}>
                  <a className="author_space">
                    <AuthorSpace data={data.author} />
                    <ContentTitle data={data.author} />
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
