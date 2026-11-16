import { Music } from 'types/internal/media/output'
import { formatTime } from 'utils/functions/datetime'
import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import Link from 'components/parts/Link'
import AudioPlayer from 'components/widgets/AudioPlayer'
import style from './Music.module.scss'
import CardMediaContent from '../Content'

interface Props {
  item: Music
}

export default function MusicCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, image, music, duration, channel } = item

  return (
    <Card className={style.card}>
      <Link href={`/media/music/${ulid}`} className={style.jacket}>
        <ExImage src={image || channel.avatar} width="195" height="195" className={style.jacket_image} />
        {duration > 0 && <span className={style.duration}>{formatTime(duration)}</span>}
      </Link>
      <AudioPlayer src={music} className={style.player} />
      <CardMediaContent href={`/media/music/${ulid}`} media={item} />
    </Card>
  )
}
