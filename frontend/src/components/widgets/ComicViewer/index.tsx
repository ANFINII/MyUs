import { useState, useCallback } from 'react'
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
    setCurrentIndex((prev) => (prev <= 0 ? pages.length - 1 : prev - 1))
  }, [pages.length])

  const handleNext = useCallback(() => {
    setCurrentIndex((prev) => (prev >= pages.length - 1 ? 0 : prev + 1))
  }, [pages.length])

  if (pages.length === 0) return <></>

  return (
    <div className={style.viewer}>
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
  )
}
