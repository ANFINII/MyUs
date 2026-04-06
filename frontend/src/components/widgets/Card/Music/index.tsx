import { Music } from 'types/internal/media'
import AudioPlayer from 'components/widgets/AudioPlayer'
import style from './Music.module.scss'
import CardMediaContent from '../Media/Content'

interface Props {
  item: Music
}

export default function MusicCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, music } = item

  return (
    <section className={style.card}>
      <AudioPlayer src={music} className={style.player} />
      <CardMediaContent href={`/media/music/${ulid}`} media={item} />
    </section>
  )
}
