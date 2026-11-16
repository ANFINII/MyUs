import { useEffect, useRef } from 'react'
import cx from 'utils/functions/cx'
import { activeLyricIndex, parseLyric } from 'utils/functions/lyric'
import style from './Lyric.module.scss'

const LOOKAHEAD_SECONDS = 0.15

interface Props {
  lyric: string
  currentTime: number
  isExpand: boolean
  onSeek: (time: number) => void
}

export default function Lyric(props: Props): React.JSX.Element {
  const { lyric, currentTime, isExpand, onSeek } = props

  const boxRef = useRef<HTMLDivElement>(null)
  const trackRef = useRef<HTMLDivElement>(null)
  const { isSynced, lines } = parseLyric(lyric)
  const activeIndex = isSynced ? activeLyricIndex(lines, currentTime + LOOKAHEAD_SECONDS) : -1

  useEffect(() => {
    const box = boxRef.current
    const track = trackRef.current
    const line = track?.querySelector<HTMLElement>(`[data-index="${Math.max(activeIndex, 0)}"]`)
    if (!box || !track || !line || !isSynced) return
    const offset = Math.max(0, line.offsetTop - box.clientHeight / 2 + line.clientHeight / 2)
    track.style.transform = `translateY(${-offset}px)`
  }, [activeIndex, isExpand, isSynced])

  return (
    <div ref={boxRef} className={cx(style.lyric, isSynced && style.synced, isExpand && style.expand)}>
      <div ref={trackRef} className={style.track}>
        {lines.map((line, index) => (
          <p
            key={`${index}-${line.time}`}
            data-index={index}
            className={cx(style.line, index === activeIndex && style.active, index < activeIndex && style.passed)}
            onClick={isSynced ? () => onSeek(line.time) : undefined}
          >
            {line.text || '\u00A0'}
          </p>
        ))}
      </div>
    </div>
  )
}
