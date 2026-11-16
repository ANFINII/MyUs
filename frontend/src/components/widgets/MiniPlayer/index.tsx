import { useMusicPlayer } from 'components/hooks/useMusicPlayer'
import ExImage from 'components/parts/ExImage'
import IconChevront from 'components/parts/Icon/Chevront'
import IconCross from 'components/parts/Icon/Cross'
import Link from 'components/parts/Link'
import AudioPlayer from 'components/widgets/AudioPlayer'
import style from './MiniPlayer.module.scss'

export default function MiniPlayer(): React.JSX.Element {
  const { current, next, prev, close } = useMusicPlayer()

  if (current === undefined) return <></>

  return (
    <div className={style.mini_player}>
      <ExImage src={current.image || current.channel.avatar} width="40" height="40" className={style.thumbnail} />
      <div className={style.info}>
        <Link href={`/media/music/${current.ulid}`} className={style.title}>
          {current.title}
        </Link>
        <span className={style.channel}>{current.channel.name}</span>
      </div>
      <button type="button" className={style.button} onClick={prev}>
        <IconChevront width="1.2em" height="1.2em" type="left" />
      </button>
      <AudioPlayer key={current.ulid} src={current.music} autoPlay isVolumeInline onEnded={next} className={style.player} />
      <button type="button" className={style.button} onClick={next}>
        <IconChevront width="1.2em" height="1.2em" type="right" />
      </button>
      <IconCross size="1.2em" className={style.close} onClick={close} />
    </div>
  )
}
