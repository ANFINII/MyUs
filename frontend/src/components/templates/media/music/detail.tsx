import { ChangeEvent, useState } from 'react'
import clsx from 'clsx'
import { MusicDetailOut } from 'types/internal/media/detail'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
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
          <AudioPlayer src={music} playbackRate={speed} />
          <div className={style.speed}>
            Speed
            <input type="range" min="0" max="2" step="0.25" value={speed} onChange={handleSpeed} className={style.range} />
            <span>{speed}</span>
          </div>
          {download && (
            <a href={music} download className={style.download}>
              <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" viewBox="0 0 16 16">
                <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z" />
                <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z" />
              </svg>
            </a>
          )}
        </div>

        <View isView={isLyricView} onView={handleLyricView} content={isLyricView ? '縮小表示' : '拡大表示'} />
        <div className={clsx(style.lyric, isLyricView && style.active)}>{lyric}</div>

        <Divide />
        <MediaDetailCommon media={{ type: 'music', ...other }} list={list} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
