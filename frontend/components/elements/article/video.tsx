import Link from 'next/link'
import AuthorSpace from 'components/elements/common/author_space'
import ContentTitle from 'components/elements/common/content_title'
import { videoType, VideoType } from 'lib/utils/type'


export default function VideoArtile(video: VideoType) {
  return (
    <article className="article_list">
      {/* {% for item in video_list %} */}
      <section className="section_list">
        <div className="main_decolation">
          <div className="video video_auto">
            <Link href={`/video/detail/${video.id}`}>
              <a>
                <video className="video-js vjs-16-9" muted width="272" height="153" controlsList="nodownload"
                // onContextMenu={'return' false;}
                poster={ video.image } data-setup="">
                  <source src="{{ video.convert.url }}#t=,16" type="video/mp4" data-label="360p" data-res="360"/>
                  <p>動画を再生するには、videoタグをサポートしたブラウザが必要です!</p>
                  <track kind="captions" src="/vtt/captions.ja.vtt" srcLang="en" label="English"/>
                  <track kind="subtitles" src="/vtt/captions.ja.vtt" srcLang="en" label="English"/>
                </video>
              </a>
            </Link>
            <Link href={`/video/detail/${video.id}`}>
              <a className="author_space">
                <AuthorSpace/>
                <ContentTitle/>
              </a>
            </Link>
          </div>
        </div>
      </section>
      {/* {% endfor %} */}
    </article>
  )
}
