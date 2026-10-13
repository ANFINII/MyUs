import { PAGE_SIZE } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'

interface OutProps {
  currentPage: number
  totalPages: number
  handlePage: (page: number) => void
}

export function usePagination(total: number, page: number): OutProps {
  const router = useRouter()
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE))
  const currentPage = Math.min(page, totalPages)

  const handlePage = (nextPage: number): void => {
    router.push({ pathname: router.pathname, query: { ...router.query, page: nextPage } })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return { currentPage, totalPages, handlePage }
}
