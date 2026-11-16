import { useState } from 'react'
import { Music } from 'types/internal/media/output'
import cx from 'utils/functions/cx'
import { formatTime } from 'utils/functions/datetime'
import { useMusicPlayer } from 'components/hooks/useMusicPlayer'
import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import style from './Music.module.scss'
import CardMediaContent from '../Content'

interface Props {
  item: Music
  items?: Music[]
}

export default function MusicCard(props: Props): React.JSX.Element {
  const { item, items = [item] } = props
  const { ulid, image, music, channel } = item

  const { current, play, toggle } = useMusicPlayer()

  const [duration, setDuration] = useState<number>(0)

  const isCurrent = current?.ulid === ulid

  const handleDuration = () => {
    if (duration > 0) return
    const audio = new Audio()
    audio.preload = 'metadata'
    audio.onloadedmetadata = () => setDuration(isFinite(audio.duration) ? audio.duration : 0)
    audio.src = music
  }

  const handlePlay = () => {
    handleDuration()
    if (isCurrent) return toggle()
    play(items, Math.max(items.findIndex((m) => m.ulid === ulid), 0))
  }

  return (
    <Card className={style.card}>
      <div className={cx(style.thumbnail_box, isCurrent && style.current)} onMouseEnter={handleDuration} onClick={handlePlay}>
        <ExImage src={image || channel.avatar} width="195" height="195" className={style.thumbnail} />
        <span className={style.play} />
        {duration > 0 && <span className={style.duration}>{formatTime(duration)}</span>}
      </div>
      <CardMediaContent href={`/media/music/${ulid}`} media={item} />
    </Card>
  )
}
