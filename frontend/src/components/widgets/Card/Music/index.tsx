import { Music } from 'types/internal/media'
import AudioPlayer from 'components/widgets/AudioPlayer'
import MediaContent from 'components/widgets/Media/Content'
import style from './Music.module.scss'

interface Props {
  data: Music
}

export default function MusicCard(props: Props): React.JSX.Element {
  const { data } = props
  const { ulid, music } = data

  return (
    <section className={style.card}>
      <AudioPlayer src={music} className={style.player} />
      <MediaContent href={`/media/music/${ulid}`} media={data} />
    </section>
  )
}
