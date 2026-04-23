import cx from 'utils/functions/cx'
import ArrowButton from './ArrowButton'
import PageButton from './PageButton'
import style from './Pagination.module.scss'

const calcPages = (current: number, total: number): (number | '...')[] => {
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  const pages: (number | '...')[] = [1]
  if (current > 3) pages.push('...')
  const start = Math.max(2, current - 1)
  const end = Math.min(total - 1, current + 1)
  for (let i = start; i <= end; i++) pages.push(i)
  if (current < total - 2) pages.push('...')
  pages.push(total)
  return pages
}

type marginType = 'mv_16' | 'mv_24' | 'mv_32' | 'mv_40'

interface Props {
  currentPage: number
  totalPages: number
  margin?: marginType
  onChange: (page: number) => void
}

export default function Pagination(props: Props): React.JSX.Element | null {
  const { currentPage, totalPages, margin = 'mv_16', onChange } = props

  const pages = calcPages(currentPage, totalPages)
  const handlePrev = () => onChange(currentPage - 1)
  const handleNext = () => onChange(currentPage + 1)
  const handlePage = (page: number) => () => onChange(page)

  return (
    <nav className={cx(style.pagination, margin)}>
      <ArrowButton type="left" disabled={currentPage === 1} onClick={handlePrev} />
      {pages.map((page, i) =>
        page === '...' ? (
          <span key={`ellipsis-${i}`} className={style.ellipsis}>
            …
          </span>
        ) : (
          <PageButton key={page} page={page} isActive={page === currentPage} onClick={handlePage(page)} />
        ),
      )}
      <ArrowButton type="right" disabled={currentPage === totalPages} onClick={handleNext} />
    </nav>
  )
}
