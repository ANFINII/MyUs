import { Music } from 'types/internal/media'
import AudioPlayer from 'components/widgets/AudioPlayer'
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
      <AudioPlayer src={music} />
      <MediaContent href={`/media/music/${ulid}`} media={media} />
    </section>
  )
}
