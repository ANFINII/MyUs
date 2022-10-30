import Head from 'next/head'
import { GetServerSideProps } from 'next'


export const getServerSideProps: GetServerSideProps = async ({ context }: any) => {
  const { id } = context.params
  const BASEURL = process.env.NEXT_PUBLIC_API_URL
  const res = await fetch(BASEURL + `/api/video/detail/${id}`)
  const data = await res.json()
  return { props: { data } }
}

export default function VideoCreate({ data }: any) {
  const image_url = process.env.NEXT_PUBLIC_API_URL + data.image
  const video_url = process.env.NEXT_PUBLIC_API_URL + data.video
  return (
    <>
      <Head>
        <title>MyUsビデオ</title>
      </Head>

      {data.publish ?
        <article className="article_detail">
          <div className="main_image_color">
            <div className="main_image">
              <video id="video" className="video vjs-fluid vjs-big-play-centered vjs-16-9" controls controlsList="nodownload"
              // onContextMenu="return false"
              poster={ image_url } data-setup='{"playbackRates": [0.5, 1, 1.25, 1.5, 2]}'>
                <source src={ video_url } type="application/x-mpegURL"/>
                <p>動画を再生するには、videoタグをサポートしたブラウザが必要です!</p>
                {/* <track kind="captions" src="{% static 'vtt/captions.ja.vtt' %}" srclang="en" label="English">
                <track kind="subtitles" src="{% static 'vtt/captions.ja.vtt' %}" srclang="en" label="English"> */}
                <p className="vjs-no-js">この動画を見るには、JavaScriptを有効にしてください!
                  <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>
                </p>
              </video>
            </div>
          </div>

          <div className="article_detail_section_side">
            <div className="article_detail_section_1">
              {/* {% include 'parts/common/common.html' %} */}
            </div>
            <div className="article_detail_section_2">
              {/* {% include 'video/video_article_detail.html' %} */}
            </div>
          </div>
        </article>
      :
        <h2 className="unpublished">非公開に設定されてます!</h2>
      }
    </>
  )
}
