import { UseQueryResult } from '@tanstack/react-query'

export function useFreshData<T>(query: UseQueryResult<T>): T | undefined {
  return query.isFetchedAfterMount ? query.data : undefined
}
