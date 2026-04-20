import { Music } from 'types/internal/media/output'
import Card from 'components/parts/Card'
import AudioPlayer from 'components/widgets/AudioPlayer'
import style from './Music.module.scss'
import CardMediaContent from '../Content'

interface Props {
  item: Music
}

export default function MusicCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, music } = item

  return (
    <Card className={style.card}>
      <AudioPlayer src={music} className={style.player} />
      <CardMediaContent href={`/media/music/${ulid}`} media={item} />
    </Card>
  )
}
