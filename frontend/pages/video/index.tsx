import Head from 'next/head'
import VideoArticle from 'components/elements/article/video'

export default function Video(props) {
  return (
    <>
      <Head>
        <title>MyUsビデオ</title>
      </Head>

      <h1>Video
        {/* {% if query %} */}
        <section className="search_message">
          {/* 「{{ props.query }}」の検索結果「{{ props.count }}」件 */}
        </section>
        {/* {% endif %} */}
      </h1>

      <VideoArticle/>

      {/* {% block extrajs %}
      <script src="https://vjs.zencdn.net/7.19.2/video.min.js"></script>
      <script src="{% static 'js/video_auto.js' %}"></script>
      {% endblock extrajs %}     */}
    </>
  )
}
