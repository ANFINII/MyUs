import { useEffect, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import { TocHeading } from 'utils/functions/toc'
import style from './BlogToc.module.scss'

interface Props {
  headings: TocHeading[]
  className?: string
}

export default function BlogToc(props: Props): React.JSX.Element {
  const { headings, className } = props

  const { t } = useTranslation()
  const [activeId, setActiveId] = useState(headings[0]?.id ?? '')
  const scrollRef = useRef<HTMLDivElement>(null)

  const topLevel = Math.min(...headings.map((heading) => heading.level))
  const activeIndex = Math.max(
    headings.findIndex((heading) => heading.id === activeId),
    0,
  )
  const progress = ((activeIndex + 1) / headings.length) * 100

  const followActive = (id: string) => {
    const container = scrollRef.current
    const button = container?.querySelector<HTMLElement>(`[data-toc-id="${id}"]`)
    if (!container || !button) return
    container.scrollTo({ top: button.offsetTop - (container.clientHeight - button.offsetHeight) / 2, behavior: 'smooth' })
  }

  useEffect(() => {
    const elements = headings.map((heading) => document.getElementById(heading.id)).filter((element) => element !== null)
    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries.find((e) => e.isIntersecting)
        if (!entry) return
        setActiveId(entry.target.id)
        followActive(entry.target.id)
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
    <nav className={cx(style.toc, className)} aria-label={t('media.blog.toc')}>
      <div className={style.header}>
        <span className={style.title}>{t('media.blog.toc')}</span>
        <span className={style.count}>
          {activeIndex + 1} / {headings.length}
        </span>
      </div>
      <div className={style.progress}>
        <div className={style.progress_bar} style={{ width: `${progress}%` }} />
      </div>
      <div ref={scrollRef} className={style.scroll}>
        <ul className={style.list}>
          {headings.map((heading, index) => (
            <li key={heading.id}>
              <button
                type="button"
                data-toc-id={heading.id}
                className={cx(style.item, heading.level === topLevel ? style.main : style.sub, index < activeIndex && style.passed, index === activeIndex && style.active)}
                onClick={() => handleHeading(heading.id)}
              >
                {heading.text}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  )
}
