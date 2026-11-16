import { useEffect } from 'react'
import { useMusicPlayer } from 'components/hooks/useMusicPlayer'
import { useRouter } from 'components/hooks/useRouter'
import ExImage from 'components/parts/ExImage'
import IconChevront from 'components/parts/Icon/Chevront'
import IconCross from 'components/parts/Icon/Cross'
import Link from 'components/parts/Link'
import AudioPlayer from 'components/widgets/AudioPlayer'
import style from './MiniPlayer.module.scss'

const PLAYER_DETAIL_PATH = /^\/media\/(video|music)\/(?!playlist$)[^/]+$/

export default function MiniPlayer(): React.JSX.Element {
  const router = useRouter()
  const { current, audioRef, next, prev, close } = useMusicPlayer()

  const isPlayerDetail = PLAYER_DETAIL_PATH.test(router.pathname)

  useEffect(() => {
    if (isPlayerDetail) close()
  }, [isPlayerDetail, close])

  if (current === undefined || isPlayerDetail) return <></>

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
      <AudioPlayer key={current.ulid} src={current.music} autoPlay isVolumeInline audioRef={audioRef} onEnded={next} className={style.player} />
      <button type="button" className={style.button} onClick={next}>
        <IconChevront width="1.2em" height="1.2em" type="right" />
      </button>
      <IconCross size="1.2em" className={style.close} onClick={close} />
    </div>
  )
}
