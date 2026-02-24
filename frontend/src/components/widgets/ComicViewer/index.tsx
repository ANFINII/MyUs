import { useState, useCallback, useEffect, useRef } from 'react'
import clsx from 'clsx'
import ExImage from 'components/parts/ExImage'
import IconChevront from 'components/parts/Icon/Chevront'
import IconFullscreen from 'components/parts/Icon/Fullscreen'
import HStack from 'components/parts/Stack/Horizontal'
import style from './ComicViewer.module.scss'

interface Props {
  pages: string[]
}

export default function ComicViewer(props: Props): React.JSX.Element {
  const { pages } = props

  const viewerRef = useRef<HTMLDivElement>(null)
  const [page, setPage] = useState(0)
  const [isFull, setIsFull] = useState(false)

  const handlePrev = useCallback(() => setPage((p) => Math.max(p - 1, 0)), [])
  const handleNext = useCallback(() => setPage((p) => Math.min(p + 1, pages.length - 1)), [pages.length])

  const handleFull = useCallback(() => {
    const viewer = viewerRef.current
    if (!viewer) return
    if (document.fullscreenElement) {
      document.exitFullscreen()
    } else {
      viewer.requestFullscreen()
    }
  }, [])

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowLeft') handlePrev()
      if (e.key === 'ArrowRight') handleNext()
      if (e.key === 'Escape' && isFull) setIsFull(false)
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [handlePrev, handleNext, isFull])

  useEffect(() => {
    const handleChange = () => setIsFull(!!document.fullscreenElement)
    document.addEventListener('fullscreenchange', handleChange)
    return () => document.removeEventListener('fullscreenchange', handleChange)
  }, [])

  if (pages.length === 0) return <></>

  return (
    <div ref={viewerRef} className={clsx(style.viewer, isFull && style.full)}>
      <div className={style.display}>
        <div className={style.prev} onClick={handlePrev}>
          <IconChevront width="32" height="32" type="left" />
        </div>
        <div className={style.page}>
          <ExImage src={pages[page]} />
        </div>
        <div className={style.next} onClick={handleNext}>
          <IconChevront width="32" height="32" type="right" />
        </div>
      </div>
      <div className={style.footer}>
        <p className={style.counter}>
          <HStack gap="1">
            <span>{page + 1}</span>
            <span>/</span>
            <span>{pages.length}</span>
          </HStack>
        </p>
        <div className={style.thumbnails}>
          {pages.map((src, index) => (
            <div key={src} className={clsx(style.thumbnail, index === page && style.active)} onClick={() => setPage(index)}>
              <ExImage src={src} />
            </div>
          ))}
        </div>
        <div className={style.full_icon} onClick={handleFull}>
          <IconFullscreen size="1.2em" />
        </div>
      </div>
    </div>
  )
}
