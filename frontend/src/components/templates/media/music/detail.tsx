import { ChangeEvent, useState } from 'react'
import { MusicDetailOut } from 'types/internal/media/detail'
import { MediaPath } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
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
  const { music, lyric, download, publish, ...other } = detail

  const { toast, handleToast } = useToast()
  const [speed, setSpeed] = useState(1)
  const [isLyricView, setIsLyricView] = useState(false)

  const handleSpeed = (e: ChangeEvent<HTMLInputElement>) => setSpeed(Number(e.target.value))
  const handleLyricView = () => setIsLyricView(!isLyricView)

  return (
    <Main metaTitle="Music" toast={toast}>
      <MediaDetail publish={publish}>
        <VStack gap="8" className={style.media_detail_music}>
          <AudioPlayer src={music} playbackRate={speed} className={style.player} />
          <HStack justify="between">
            <SpeedControl value={speed} onChange={handleSpeed} />
            {download && (
              <a href={music} download className={style.download}>
                <IconDownload size="1.5em" />
              </a>
            )}
          </HStack>
        </VStack>
        {lyric && (
          <>
            <View isView={isLyricView} onView={handleLyricView} content={isLyricView ? '縮小表示' : '拡大表示'} />
            <div className={cx(style.lyric, isLyricView && style.active)}>{lyric}</div>
          </>
        )}
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Music, ...other }} list={list} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
