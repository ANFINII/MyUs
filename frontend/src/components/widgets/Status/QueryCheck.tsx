import { UseQueryResult } from '@tanstack/react-query'
import ErrorCheck from './Check'
import PageLoading from './Loading'

type Queries = Record<string, UseQueryResult<unknown>>

type QueryData<T extends Queries> = { [K in keyof T]: T[K] extends UseQueryResult<infer D> ? D : never }

interface Props<T extends Queries> {
  title?: string
  queries: T
  children: React.ReactNode | ((data: QueryData<T>) => React.ReactNode)
}

export default function QueryCheck<T extends Queries>(props: Props<T>): React.JSX.Element {
  const { title, queries, children } = props

  const results = Object.values(queries)
  const error = results.find((q) => q.error !== null)?.error ?? null
  const isReady = results.every((q) => q.data !== undefined)

  const render = (): React.ReactNode => {
    if (typeof children !== 'function') return children
    const data = Object.fromEntries(Object.entries(queries).map(([key, q]) => [key, q.data])) as QueryData<T>
    return children(data)
  }

  return <ErrorCheck error={error}>{isReady ? render() : <PageLoading title={title} />}</ErrorCheck>
}
