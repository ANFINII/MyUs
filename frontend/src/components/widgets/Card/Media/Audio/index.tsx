import { useState } from 'react'
import { Audio } from 'types/internal/media/output'
import cx from 'utils/functions/cx'
import { formatTime } from 'utils/functions/datetime'
import { useAudioPlayer } from 'components/hooks/useAudioPlayer'
import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import PlaylistAdd from 'components/widgets/PlaylistAdd'
import style from './Audio.module.scss'
import CardMediaContent from '../Content'

interface Props {
  item: Audio
  items?: Audio[]
}

export default function AudioCard(props: Props): React.JSX.Element {
  const { item, items = [item] } = props
  const { ulid, image, audio, channel } = item

  const { current, play, toggle } = useAudioPlayer()
  const [duration, setDuration] = useState<number>(0)

  const isCurrent = current?.ulid === ulid

  const handleDuration = () => {
    if (duration > 0) return
    const element = document.createElement('audio')
    element.preload = 'metadata'
    element.onloadedmetadata = () => setDuration(isFinite(element.duration) ? element.duration : 0)
    element.src = audio
  }

  const handlePlay = () => {
    handleDuration()
    if (isCurrent) return toggle()
    play(
      items,
      Math.max(
        items.findIndex((m) => m.ulid === ulid),
        0,
      ),
    )
  }

  return (
    <Card className={style.card}>
      <div className={cx(style.thumbnail_box, isCurrent && style.current)} onMouseEnter={handleDuration} onClick={handlePlay}>
        <ExImage src={image || channel.avatar} width="195" height="195" className={style.thumbnail} />
        <span className={style.play} />
        {duration > 0 && <span className={style.duration}>{formatTime(duration)}</span>}
      </div>
      <PlaylistAdd audioUlid={ulid} className={style.playlist_add} />
      <CardMediaContent href={`/media/audio/${ulid}`} media={item} />
    </Card>
  )
}
