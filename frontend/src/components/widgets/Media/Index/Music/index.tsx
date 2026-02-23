import { Music } from 'types/internal/media'
import MediaContent from 'components/widgets/Media/Content'
import style from './Music.module.scss'

interface Props {
  media: Music
}

export default function MediaMusic(props: Props): React.JSX.Element {
  const { media } = props
  const { ulid, music } = media

  return (
    <section className={style.media}>
      <audio controls controlsList="nodownload" preload="none" className="audio_auto">
        <source src={music} />
        <p>ブラウザがaudioに対応しておりません</p>
      </audio>
      <div className={style.content}>
        <MediaContent href={`/media/music/${ulid}`} media={media} />
      </div>
    </section>
  )
}
