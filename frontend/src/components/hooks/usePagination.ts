import { useEffect, useMemo, useState } from 'react'

interface UsePaginationResult<T> {
  currentPage: number
  totalPages: number
  pageDatas: T[]
  handlePage: (page: number) => void
}

export const usePagination = <T>(datas: T[], pageSize: number): UsePaginationResult<T> => {
  const [currentPage, setCurrentPage] = useState<number>(1)

  useEffect(() => setCurrentPage(1), [datas])

  const totalPages = Math.ceil(datas.length / pageSize)

  const pageDatas = useMemo(() => {
    const start = (currentPage - 1) * pageSize
    return datas.slice(start, start + pageSize)
  }, [datas, currentPage, pageSize])

  const handlePage = (page: number) => setCurrentPage(page)

  return { currentPage, totalPages, pageDatas, handlePage }
}
