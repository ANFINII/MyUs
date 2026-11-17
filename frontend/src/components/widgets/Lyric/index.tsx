import { useEffect, useRef } from 'react'
import cx from 'utils/functions/cx'
import { activeLyricIndex, parseLyric } from 'utils/functions/lyric'
import style from './Lyric.module.scss'

const LOOKAHEAD_SECONDS = 0.15
const SCROLL_MS = 700
const USER_SCROLL_PAUSE_MS = 3000

const easeOutQuint = (t: number): number => 1 - Math.pow(1 - t, 5)

interface Props {
  lyric: string
  currentTime: number
  isExpand: boolean
  className?: string
  onSeek: (time: number) => void
}

export default function Lyric(props: Props): React.JSX.Element {
  const { lyric, currentTime, isExpand, className, onSeek } = props

  const boxRef = useRef<HTMLDivElement>(null)
  const frameRef = useRef<number>(0)
  const userScrollRef = useRef<number>(0)
  const { isSynced, lines } = parseLyric(lyric)
  const activeIndex = isSynced ? activeLyricIndex(lines, currentTime + LOOKAHEAD_SECONDS) : -1

  const handleUserScroll = () => {
    userScrollRef.current = Date.now()
    cancelAnimationFrame(frameRef.current)
  }

  useEffect(() => {
    const box = boxRef.current
    const line = box?.querySelector<HTMLElement>(`[data-index="${Math.max(activeIndex, 0)}"]`)
    if (!box || !line || !isSynced || Date.now() - userScrollRef.current < USER_SCROLL_PAUSE_MS) return
    const from = box.scrollTop
    const to = Math.max(0, line.offsetTop - box.clientHeight / 2 + line.clientHeight / 2)
    const start = performance.now()
    const step = (now: number) => {
      const progress = Math.min(1, (now - start) / SCROLL_MS)
      box.scrollTop = from + (to - from) * easeOutQuint(progress)
      if (progress < 1) frameRef.current = requestAnimationFrame(step)
    }
    cancelAnimationFrame(frameRef.current)
    frameRef.current = requestAnimationFrame(step)
    return () => cancelAnimationFrame(frameRef.current)
  }, [activeIndex, isExpand, isSynced])

  return (
    <div ref={boxRef} className={cx(style.lyric, isSynced && style.synced, isExpand && style.expand, className)} onWheel={handleUserScroll} onTouchMove={handleUserScroll}>
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
