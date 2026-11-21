import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import { TocHeading } from 'utils/functions/toc'
import style from './BlogToc.module.scss'

interface Props {
  headings: TocHeading[]
}

export default function BlogToc(props: Props): React.JSX.Element {
  const { headings } = props

  const { t } = useTranslation()
  const [activeId, setActiveId] = useState(headings[0]?.id ?? '')

  const topLevel = Math.min(...headings.map((heading) => heading.level))
  const activeIndex = Math.max(
    headings.findIndex((heading) => heading.id === activeId),
    0,
  )
  const progress = ((activeIndex + 1) / headings.length) * 100

  useEffect(() => {
    const elements = headings.map((heading) => document.getElementById(heading.id)).filter((element) => element !== null)
    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries.find((e) => e.isIntersecting)
        if (entry) setActiveId(entry.target.id)
      },
      { rootMargin: '0px 0px -70% 0px' },
    )
    elements.forEach((element) => observer.observe(element))
    return () => observer.disconnect()
  }, [headings])

  const handleHeading = (id: string) => {
    setActiveId(id)
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  return (
    <nav className={style.toc} aria-label={t('media.blog.toc')}>
      <div className={style.header}>
        <span className={style.title}>{t('media.blog.toc')}</span>
        <span className={style.count}>
          {activeIndex + 1} / {headings.length}
        </span>
      </div>
      <div className={style.progress}>
        <div className={style.progress_bar} style={{ width: `${progress}%` }} />
      </div>
      <ul className={style.list}>
        {headings.map((heading, index) => (
          <li key={heading.id}>
            <button
              type="button"
              className={cx(style.item, heading.level === topLevel ? style.main : style.sub, index < activeIndex && style.passed, index === activeIndex && style.active)}
              onClick={() => handleHeading(heading.id)}
            >
              {heading.text}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  )
}
