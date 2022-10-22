import Head from 'next/head'
import VideoArticle from 'components/elements/article/video'
import { GetServerSideProps } from 'next'

export async function getVideoList() {
  const BASEURL = process.env.NEXT_PUBLIC_API_URL
  const res = await fetch(BASEURL + '/api/video')
  const data = await res.json()
  return data
}

export const getServerSideProps: GetServerSideProps = async () => {
  const data = await getVideoList()
  return {
    props: { data },
  };
}

export default function Video(data: any) {
  return (
    <>
      <Head>
        <title>MyUsビデオ</title>
      </Head>

      <h1>Video
        {/* {% if query %} */}
        {/* <section className="search_message"> */}
          {/* 「{{ props.query }}」の検索結果「{{ props.count }}」件 */}
        {/* </section> */}
        {/* {% endif %} */}
      </h1>

      <VideoArticle datas={data} />

      {/* {% block extrajs %}
      <script src="https://vjs.zencdn.net/7.19.2/video.min.js"></script>
      <script src="{% static 'js/video_auto.js' %}"></script>
      {% endblock extrajs %}     */}
    </>
  )
}
