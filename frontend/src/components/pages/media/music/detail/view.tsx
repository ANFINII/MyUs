import { ChangeEvent, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { MusicDetailOut } from 'types/internal/media/output'
import { RepeatMode } from 'types/internal/other'
import { getMusicHiresUrl } from 'api/internal/media/detail'
import { FetchError, MediaPath } from 'utils/constants/enum'
import { hiresLabel } from 'utils/functions/hires'
import { useLoading } from 'components/hooks/useLoading'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Divide from 'components/parts/Divide'
import ExImage from 'components/parts/ExImage'
import SpeedControl from 'components/parts/SpeedControl'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import AudioPlayer from 'components/widgets/AudioPlayer'
import Lyric from 'components/widgets/Lyric'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import Paywall from 'components/widgets/Paywall'
import PlaylistAdd from 'components/widgets/PlaylistAdd'
import View from 'components/widgets/View'
import style from './Detail.module.scss'

interface Props {
  data: MusicDetailOut
}

export default function MusicDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list, series } = data
  const { image, music, gain, lyric, publish, isPurchased, hires, product, ...other } = detail

  const router = useRouter()
  const { t } = useTranslation()
  const { user } = useUser()
  const { toast, handleToast } = useToast()
  const { loading, handleLoading } = useLoading()
  const [speed, setSpeed] = useState<number>(1)
  const [isLyricView, setIsLyricView] = useState<boolean>(false)
  const [repeat, setRepeat] = useState<RepeatMode>('off')
  const [currentTime, setCurrentTime] = useState<number>(0)
  const audioRef = useRef<HTMLAudioElement>(null)

  const isOwner = user.isActive && user.ulid === other.channel.ownerUlid

  const handleSpeed = (e: ChangeEvent<HTMLInputElement>) => setSpeed(Number(e.target.value))
  const handleLyricView = () => setIsLyricView(!isLyricView)
  const handleRepeat = () => setRepeat(repeat === 'off' ? 'one' : 'off')

  const handleDownload = async () => {
    handleLoading(true)
    const ret = await getMusicHiresUrl(other.ulid)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(errorMessage(ret.error, FetchError.Get), true)
      return
    }
    router.push(ret.value.url)
  }

  const handleSeek = (time: number) => {
    const audio = audioRef.current
    if (!audio) return
    audio.currentTime = time
    audio.play()?.catch(() => {})
  }

  return (
    <Main metaTitle="Music" toast={toast}>
      <MediaDetail publish={publish}>
        <div className={style.media_detail_music}>
          <div className={style.thumbnail_box}>
            <ExImage src={image || other.channel.avatar} className={style.thumbnail} />
          </div>
          <VStack gap="6" className={style.controls}>
            <AudioPlayer src={music} gain={gain} playbackRate={speed} isVolumeInline repeat={repeat} audioRef={audioRef} onTimeUpdate={setCurrentTime} onRepeat={handleRepeat} />
            <HStack justify="between">
              <SpeedControl value={speed} onChange={handleSpeed} className={style.speed} />
              <div className={style.actions}>
                <PlaylistAdd musicUlid={other.ulid} />
              </div>
            </HStack>
          </VStack>
        </div>
        {hires !== null && product !== null && (isOwner || isPurchased) && (
          <section className={style.hires}>
            <p className={style.hires_title}>{t('media.music.hiresTitle')}</p>
            <p className={style.hires_label}>{hiresLabel(hires)}</p>
            <Button color="green" size="s" name={t('media.music.hiresDownload')} loading={loading} onClick={handleDownload} />
          </section>
        )}
        {hires !== null && product !== null && !isOwner && !isPurchased && (
          <Paywall title={t('media.music.hiresTitle')} label={hiresLabel(hires)} notice={t('media.music.hiresNotice')} product={product} handleToast={handleToast} />
        )}
        {lyric && (
          <>
            <View isView={isLyricView} onView={handleLyricView} content={isLyricView ? t('view.collapse') : t('view.expand')} />
            <Lyric lyric={lyric} currentTime={currentTime} isExpand={isLyricView} onSeek={handleSeek} />
          </>
        )}
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Music, ...other }} list={list} series={series} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
