import { Search } from 'types/internal/media/output'
import { useRouter } from 'components/hooks/useRouter'

export function useSearch(count: number): Search {
  const router = useRouter()
  const name = router.query.search?.toString() ?? ''
  return { name, count }
}
