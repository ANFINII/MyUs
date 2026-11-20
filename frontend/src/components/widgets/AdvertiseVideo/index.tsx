import { MouseEvent, SyntheticEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Advertise } from 'types/internal/advertise'
import { postAdvertiseRead } from 'api/internal/advertise'
import { isHttpsUrl } from 'utils/functions/validation'
import style from './AdvertiseVideo.module.scss'

const SKIP_SECONDS = 5

interface Props {
  item: Advertise
  onEnd: () => void
}

export default function AdvertiseVideo(props: Props): React.JSX.Element {
  const { item, onEnd } = props
  const { ulid, url, title, image, video } = item

  const { t } = useTranslation()
  const [remain, setRemain] = useState<number>(SKIP_SECONDS)
  const [isMuted, setIsMuted] = useState<boolean>(true)

  const handleTime = (e: SyntheticEvent<HTMLVideoElement>) => setRemain(Math.max(SKIP_SECONDS - Math.floor(e.currentTarget.currentTime), 0))
  const handlePlay = (e: MouseEvent<HTMLVideoElement>) => e.currentTarget.paused && e.currentTarget.play()
  const handleMute = () => setIsMuted(!isMuted)
  const handleRead = () => postAdvertiseRead(ulid)

  return (
    <div className={style.advertise}>
      <video src={video} poster={image} autoPlay muted={isMuted} playsInline className={style.video} onClick={handlePlay} onTimeUpdate={handleTime} onEnded={onEnd} onError={onEnd} />
      <span className={style.badge}>{t('advertise.badge')}</span>
      <a href={isHttpsUrl(url) ? url : undefined} target="_blank" rel="noopener noreferrer" className={style.link} onClick={handleRead}>
        {title}
      </a>
      <button type="button" className={style.mute} onClick={handleMute}>
        {isMuted ? t('advertise.unmute') : t('advertise.mute')}
      </button>
      {remain > 0 ? (
        <span className={style.wait}>{t('advertise.skipIn', { count: remain })}</span>
      ) : (
        <button type="button" className={style.skip} onClick={onEnd}>
          {t('advertise.skip')}
        </button>
      )}
    </div>
  )
}
