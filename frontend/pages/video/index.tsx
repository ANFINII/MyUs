import Head from 'next/head'
import Link from 'next/link'
import AuthorSpace from 'components/elements/author_space'
import ContentTitle from 'components/elements/content_title'

export default function Video(props) {
  return (
    <>
      <Head>
        <title>MyUsビデオ</title>
      </Head>

      <h1>Video
        {/* {% if query %} */}
        <section className="messages_search">
          {/* 「{{ props.query }}」の検索結果「{{ props.count }}」件 */}
        </section>
        {/* {% endif %} */}
      </h1>

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

      {/* {% block extrajs %}
      <script src="https://vjs.zencdn.net/7.19.2/video.min.js"></script>
      <script src="{% static 'js/video_auto.js' %}"></script>
      {% endblock extrajs %}     */}
    </>
  )
}
