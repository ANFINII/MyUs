import Link from 'next/link'
import { Video } from 'types/internal/media'
import MediaContent from 'components/widgets/Common/MediaContent'
import style from './MediaContent.module.scss'

interface Props {
  data: Video
}

export default function MediaVideo(props: Props) {
  const { data } = props
  const { id, title, image, convert, read, like, created, author } = data

  return (
    <section className={style.section_list}>
      <div className={style.decolation}>
        <div className="video video_auto">
          <Link href={`/media/video/${id}`}>
            <video className="video-js" muted width={272} height={153} controlsList="nodownload" poster={image} data-setup="">
              {/* onContextMenu="return false" */}
              <source src={convert} type="video/mp4" data-label="360p" data-res="360" />
              <p>動画を再生するには、videoタグをサポートしたブラウザが必要です!</p>
              <track kind="captions" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
              <track kind="subtitles" src="/vtt/captions.ja.vtt" srcLang="en" label="English" />
            </video>
            <MediaContent author={author} title={title} read={read} totalLike={like} created={created} />
          </Link>
        </div>
      </div>
    </section>
  )
}
