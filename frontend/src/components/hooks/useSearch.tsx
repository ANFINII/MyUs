import { Search } from 'types/internal/media/output'
import { useRouter } from 'components/hooks/useRouter'

export function useSearch(count: number): Search {
  const router = useRouter()
  const name = String(router.query.search ?? '')
  return { name, count }
}
