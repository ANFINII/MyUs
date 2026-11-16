import { useEffect, useRef } from 'react'
import cx from 'utils/functions/cx'
import { activeLyricIndex, parseLyric } from 'utils/functions/lyric'
import style from './Lyric.module.scss'

interface Props {
  lyric: string
  currentTime: number
  isExpand: boolean
  onSeek: (time: number) => void
}

export default function Lyric(props: Props): React.JSX.Element {
  const { lyric, currentTime, isExpand, onSeek } = props

  const boxRef = useRef<HTMLDivElement>(null)
  const { isSynced, lines } = parseLyric(lyric)
  const activeIndex = isSynced ? activeLyricIndex(lines, currentTime) : -1

  useEffect(() => {
    const box = boxRef.current
    const line = box?.querySelector<HTMLElement>(`[data-index="${activeIndex}"]`)
    if (!box || !line) return
    box.scrollTo({ top: line.offsetTop - box.clientHeight / 2 + line.clientHeight / 2, behavior: 'smooth' })
  }, [activeIndex])

  return (
    <div ref={boxRef} className={cx(style.lyric, isSynced && style.synced, isExpand && style.expand)}>
      {lines.map((line, index) => (
        <p
          key={`${index}-${line.time}`}
          data-index={index}
          className={cx(style.line, index === activeIndex && style.active, index < activeIndex && style.passed)}
          onClick={isSynced ? () => onSeek(line.time) : undefined}
        >
          {line.text || ' '}
        </p>
      ))}
    </div>
  )
}
