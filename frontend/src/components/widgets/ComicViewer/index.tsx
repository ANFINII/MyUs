import { useState, useCallback } from 'react'
import clsx from 'clsx'
import ExImage from 'components/parts/ExImage'
import IconChevront from 'components/parts/Icon/Chevront'
import style from './ComicViewer.module.scss'

interface Props {
  pages: string[]
  title: string
}

export default function ComicViewer(props: Props): React.JSX.Element {
  const { pages, title } = props

  const [currentIndex, setCurrentIndex] = useState(0)

  const handlePrev = useCallback(() => {
    setCurrentIndex((prev) => Math.max(prev - 1, 0))
  }, [])

  const handleNext = useCallback(() => {
    setCurrentIndex((prev) => Math.min(prev + 1, pages.length - 1))
  }, [pages.length])

  if (pages.length === 0) return <></>

  return (
    <div className={style.viewer}>
      <div className={style.display}>
        <div className={style.prev} onClick={handlePrev}>
          <IconChevront width="32" height="32" type="left" />
        </div>
        <div className={style.page}>
          <ExImage src={pages[currentIndex]} title={`${title} - ${currentIndex + 1}`} />
        </div>
        <div className={style.next} onClick={handleNext}>
          <IconChevront width="32" height="32" type="right" />
        </div>
      </div>
      <div className={style.footer}>
        <p className={style.counter}>
          {currentIndex + 1} / {pages.length}
        </p>
        <div className={style.thumbnails}>
          {pages.map((src, index) => (
            <div key={src} className={clsx(style.thumbnail, index === currentIndex && style.active)} onClick={() => setCurrentIndex(index)}>
              <ExImage src={src} title={`${title} - ${index + 1}`} />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
