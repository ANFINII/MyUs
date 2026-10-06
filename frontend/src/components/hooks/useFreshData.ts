import { UseQueryResult } from '@tanstack/react-query'

type FreshData<T> = { [K in keyof T]: T[K] extends UseQueryResult<infer D> ? D : never }

export function useFreshData<T extends Record<string, UseQueryResult<unknown>>>(queries: T): FreshData<T> | undefined {
  const entries = Object.entries(queries)
  if (!entries.every(([, q]) => q.isFetchedAfterMount && q.data !== undefined)) return undefined
  return Object.fromEntries(entries.map(([key, q]) => [key, q.data])) as FreshData<T>
}
