import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import { TocHeading } from 'utils/functions/toc'
import style from './Mobile.module.scss'

interface Props {
  headings: TocHeading[]
  className?: string
}

export default function BlogTocMobile(props: Props): React.JSX.Element {
  const { headings, className } = props

  const { t } = useTranslation()

  const topLevel = Math.min(...headings.map((heading) => heading.level))

  const handleHeading = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  return (
    <details className={cx(style.toc, className)}>
      <summary className={style.summary}>
        <span>{t('media.blog.toc')}</span>
        <span className={style.count}>{headings.length}</span>
      </summary>
      <ol className={style.list}>
        {headings.map((heading) => (
          <li key={heading.id}>
            <button type="button" className={cx(style.item, heading.level === topLevel && style.main)} onClick={() => handleHeading(heading.id)}>
              {heading.text}
            </button>
          </li>
        ))}
      </ol>
    </details>
  )
}
