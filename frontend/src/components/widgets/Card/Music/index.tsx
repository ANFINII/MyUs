import { Music } from 'types/internal/media'
import AudioPlayer from 'components/widgets/AudioPlayer'
import MediaContent from 'components/widgets/Media/Content'
import style from './Music.module.scss'

interface Props {
  item: Music
}

export default function MusicCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, music } = item

  return (
    <section className={style.card}>
      <AudioPlayer src={music} className={style.player} />
      <MediaContent href={`/media/music/${ulid}`} media={item} />
    </section>
  )
}
