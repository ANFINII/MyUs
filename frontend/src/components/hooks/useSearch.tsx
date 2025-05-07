import { useRouter } from 'next/router'
import { Search } from 'types/internal/media'

export function useSearch(datas: unknown[]): Search {
  const router = useRouter()
  const query = router.query
  const name = typeof query.search === 'string' && query.search ? query.search : ''
  return { name, count: datas.length }
}
