import Link from 'next/link'
import { Video } from 'types/internal/media'
import MediaContent from 'components/widgets/Media/Content'
import style from './Media.module.scss'

interface Props {
  media: Video
}

export default function MediaVideo(props: Props): JSX.Element {
  const { media } = props
  const { id, image, convert } = media

  return (
    <section className={style.media}>
      <div className="video video_auto">
        <Link href={`/media/video/${id}`}>
          <video className="video-js" muted width="272" height="153" controlsList="nodownload" poster={image} data-setup="">
            {/* onContextMenu="return false" */}
            <source src={convert} type="video/mp4" data-label="360p" data-res="360" />
            <p>動画を再生するには、videoタグをサポートしたブラウザが必要です!</p>
            <track kind="captions" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
            <track kind="subtitles" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
          </video>
        </Link>
        <div className={style.media_content}>
          <MediaContent href={`/media/video/${id}`} media={media} />
        </div>
      </div>
    </section>
  )
}
