import { Search } from 'types/internal/media/output'
import { useAppRouter } from 'components/hooks/useAppRouter'

export function useSearch(count: number): Search {
  const router = useAppRouter()
  const query = router.query
  const name = typeof query.search === 'string' && query.search ? query.search : ''
  return { name, count }
}
