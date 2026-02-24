import { ChangeEvent, useState } from 'react'
import clsx from 'clsx'
import { MusicDetailOut } from 'types/internal/media/detail'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import IconDownload from 'components/parts/Icon/Download'
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
        <div className={style.media_detail_music}>
          <AudioPlayer src={music} playbackRate={speed} className={style.player} />
          <div className={style.speed}>
            Speed
            <input type="range" min="0" max="2" step="0.25" value={speed} onChange={handleSpeed} className={style.range} />
            <span>{speed}</span>
          </div>
          {download && (
            <a href={music} download className={style.download}>
              <IconDownload size="1.5em" />
            </a>
          )}
        </div>
        {lyric && (
          <>
            <View isView={isLyricView} onView={handleLyricView} content={isLyricView ? '縮小表示' : '拡大表示'} />
            <div className={clsx(style.lyric, isLyricView && style.active)}>{lyric}</div>
          </>
        )}
        <Divide />
        <MediaDetailCommon media={{ type: 'music', ...other }} list={list} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
