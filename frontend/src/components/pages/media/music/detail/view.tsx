import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { MusicDetailOut } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import ExImage from 'components/parts/ExImage'
import IconDownload from 'components/parts/Icon/Download'
import SpeedControl from 'components/parts/SpeedControl'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import AudioPlayer from 'components/widgets/AudioPlayer'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import View from 'components/widgets/View'
import style from './Detail.module.scss'

interface Props {
  data: MusicDetailOut
}

export default function MusicDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list } = data
  const { image, music, lyric, download, publish, ...other } = detail

  const { t } = useTranslation()
  const { toast, handleToast } = useToast()
  const [speed, setSpeed] = useState<number>(1)
  const [isLyricView, setIsLyricView] = useState<boolean>(false)

  const handleSpeed = (e: ChangeEvent<HTMLInputElement>) => setSpeed(Number(e.target.value))
  const handleLyricView = () => setIsLyricView(!isLyricView)

  return (
    <Main metaTitle="Music" toast={toast}>
      <MediaDetail publish={publish}>
        <div className={style.media_detail_music}>
          <div className={style.thumbnail_box}>
            <ExImage src={image || other.channel.avatar} className={style.thumbnail} />
          </div>
          <VStack gap="6" className={style.controls}>
            <AudioPlayer src={music} playbackRate={speed} isVolumeInline className={style.player} />
            <HStack justify="between">
              <SpeedControl value={speed} onChange={handleSpeed} className={style.speed} />
              {download && (
                <a href={music} download className={style.download}>
                  <IconDownload size="1.5em" />
                </a>
              )}
            </HStack>
          </VStack>
        </div>
        {lyric && (
          <>
            <View isView={isLyricView} onView={handleLyricView} content={isLyricView ? t('view.collapse') : t('view.expand')} />
            <div className={cx(style.lyric, isLyricView && style.active)}>{lyric}</div>
          </>
        )}
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Music, ...other }} list={list} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
