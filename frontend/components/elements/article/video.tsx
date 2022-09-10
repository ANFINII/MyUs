import Link from 'next/link'
import AuthorSpace from 'components/elements/common/author_space'
import ContentTitle from 'components/elements/common/content_title'

export default function VideoArtile(props) {
  return (
    <article className="main_article">
      {/* {% for item in video_list %} */}
      <section className="main_content">
        <div className="main_decolation">
          <div className="video video_auto">
            <Link href="/video/detail/[id][title]">
              <a>
                {/* <video className="video-js vjs-16-9" muted width="272" height="153" controlsList="nodownload" onContextMenu={return: false;} poster="{{ item.image.url }}" data-setup=""> */}
                  <source src="{{ item.convert.url }}#t=,16" type="video/mp4" data-label="360p" data-res="360"/>
                  <p>動画を再生するには、videoタグをサポートしたブラウザが必要です!</p>
                  <track kind="captions" src="/vtt/captions.ja.vtt" srcLang="en" label="English"/>
                  <track kind="subtitles" src="/vtt/captions.ja.vtt" srcLang="en" label="English"/>
                {/* </video> */}
              </a>
            </Link>
            <a href="{% url 'myus:video_detail' item.pk item.title %}" className="author_space">
              <AuthorSpace/>
              <ContentTitle/>
            </a>
          </div>
        </div>
      </section>
      {/* {% endfor %} */}
    </article>
  )
}
