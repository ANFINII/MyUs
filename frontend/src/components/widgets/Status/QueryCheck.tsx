import { UseQueryResult } from '@tanstack/react-query'
import ErrorCheck from './Check'
import PageLoading from './Loading'

type Queries = Record<string, UseQueryResult<unknown>>

type QueryData<T extends Queries> = { [K in keyof T]: T[K] extends UseQueryResult<infer D> ? D : never }

interface Props<T extends Queries> {
  title?: string
  queries: T
  fresh?: boolean
  children: React.ReactNode | ((data: QueryData<T>) => React.ReactNode)
}

export default function QueryCheck<T extends Queries>(props: Props<T>): React.JSX.Element {
  const { title, queries, fresh = false, children } = props

  const results = Object.values(queries)
  const status = results.find((q) => q.error !== null)?.error?.status ?? 200
  const isReady = results.every((q) => q.data !== undefined && (!fresh || q.isFetchedAfterMount))

  const render = (): React.ReactNode => {
    if (typeof children !== 'function') return children
    const data = Object.fromEntries(Object.entries(queries).map(([key, q]) => [key, q.data])) as QueryData<T>
    return children(data)
  }

  return <ErrorCheck status={status}>{isReady ? render() : <PageLoading title={title} />}</ErrorCheck>
}
