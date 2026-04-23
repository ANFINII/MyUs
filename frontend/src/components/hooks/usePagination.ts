import { useRouter } from 'next/router'
import { PAGE_SIZE } from 'utils/functions/common'

interface ServerPagination {
  currentPage: number
  totalPages: number
  handlePage: (page: number) => void
}

export function usePagination(total: number, page: number): ServerPagination {
  const router = useRouter()
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE))
  const currentPage = Math.min(page, totalPages)

  const handlePage = (p: number) => {
    router.push({ pathname: router.pathname, query: { ...router.query, page: p } })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return { currentPage, totalPages, handlePage }
}
