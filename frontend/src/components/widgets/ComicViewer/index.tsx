import { useState } from 'react'
import clsx from 'clsx'
import ExImage from 'components/parts/ExImage'
import IconChevront from 'components/parts/Icon/Chevront'
import style from './ComicViewer.module.scss'

interface Props {
  pages: string[]
}

export default function ComicViewer(props: Props): React.JSX.Element {
  const { pages } = props

  const [page, setPage] = useState(0)

  const handlePrev = () => setPage((prev) => Math.max(prev - 1, 0))
  const handleNext = () => setPage((prev) => Math.min(prev + 1, pages.length - 1))

  if (pages.length === 0) return <></>

  return (
    <div className={style.viewer}>
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
          {page + 1} / {pages.length}
        </p>
        <div className={style.thumbnails}>
          {pages.map((src, index) => (
            <div key={src} className={clsx(style.thumbnail, index === page && style.active)} onClick={() => setPage(index)}>
              <ExImage src={src} />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
