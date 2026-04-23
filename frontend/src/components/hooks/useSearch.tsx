import { useRouter } from 'next/router'
import { Search } from 'types/internal/media/output'

export function useSearch(count: number): Search {
  const router = useRouter()
  const query = router.query
  const name = typeof query.search === 'string' && query.search ? query.search : ''
  return { name, count }
}
