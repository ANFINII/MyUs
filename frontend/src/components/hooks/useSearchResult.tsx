import { useSearch } from '@tanstack/react-router'
import { Search } from 'types/internal/media/output'

export function useSearchResult(count: number): Search {
  const { search } = useSearch({ strict: false })
  return { name: search ?? '', count }
}
