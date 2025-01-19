import { Video } from 'types/internal/media'
import Meta from 'components/layout/Head/Meta'
import Main from 'components/layout/Main'

interface Props {
  video: Video
}

export default function VideDetailPage(props: Props): JSX.Element {
  const { video } = props
  const { image, convert, publish } = video

  return (
    <Main>
      <Meta title="Video" />
      {publish ? (
        <article className="media_detail">
          <div className="media_detail_picture">
            <div className="media_detail_contents">
              <video
                id="video"
                className="video vjs-fluid vjs-big-play-centered vjs-16-9"
                controls
                controlsList="nodownload"
                // onContextMenu="return false"
                poster={image}
                data-setup='{"playbackRates": [0.5, 1, 1.25, 1.5, 2]}'
              >
                <source src={convert} type="application/x-mpegURL" />
                <p>動画を再生するには、videoタグをサポートしたブラウザが必要です!</p>
                {/* <track kind="captions" src="{% static 'vtt/captions.ja.vtt' %}" srclang="en" label="English">
                <track kind="subtitles" src="{% static 'vtt/captions.ja.vtt' %}" srclang="en" label="English"> */}
                <p className="vjs-no-js">
                  この動画を見るには、JavaScriptを有効にしてください!
                  {/* <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a> */}
                </p>
              </video>
            </div>
          </div>

          <div className="media_detail_grid_music">
            <div>{/* {% include 'parts/common/common.html' %} */}</div>
            <div className="ml_20">{/* {% include 'video/video_article_detail.html' %} */}</div>
          </div>
        </article>
      ) : (
        <h2 className="unpublished">非公開に設定されてます!</h2>
      )}
    </Main>
  )
}
