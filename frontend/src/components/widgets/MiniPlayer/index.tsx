import { useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import { useMusicPlayer } from 'components/hooks/useMusicPlayer'
import { useRouter } from 'components/hooks/useRouter'
import ExImage from 'components/parts/ExImage'
import IconChevront from 'components/parts/Icon/Chevront'
import IconCross from 'components/parts/Icon/Cross'
import IconShuffle from 'components/parts/Icon/Shuffle'
import Link from 'components/parts/Link'
import AudioPlayer from 'components/widgets/AudioPlayer'
import style from './MiniPlayer.module.scss'

const PLAYER_DETAIL_PATH = /^\/media\/(video|music)\/[^/]+$/

export default function MiniPlayer(): React.JSX.Element {
  const router = useRouter()
  const { t } = useTranslation()
  const { current, audioRef, isShuffle, repeat, next, prev, toggleShuffle, toggleRepeat, close } = useMusicPlayer()

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
      <button type="button" title={t('player.shuffle')} className={cx(style.button, isShuffle && style.active)} onClick={toggleShuffle}>
        <IconShuffle size="1.1em" />
      </button>
      <button type="button" className={style.button} onClick={prev}>
        <IconChevront width="1.2em" height="1.2em" type="left" />
      </button>
      <AudioPlayer key={current.ulid} src={current.music} gain={current.gain} autoPlay isVolumeInline audioRef={audioRef} repeat={repeat} onEnded={next} onRepeat={toggleRepeat} className={style.player} />
      <button type="button" className={style.button} onClick={next}>
        <IconChevront width="1.2em" height="1.2em" type="right" />
      </button>
      <IconCross size="1.2em" className={style.close} onClick={close} />
    </div>
  )
}
