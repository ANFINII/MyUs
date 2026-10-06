import { ApiError } from 'lib/error'
import ErrorCheck from './Check'
import PageLoading from './Loading'

type QueryState = { error: ApiError | null }

interface Props<T> {
  queries: QueryState[]
  data: T | undefined
  title?: string
  children: React.ReactNode | ((data: T) => React.ReactNode)
}

// エラー → 取得中 → 表示の順に判定し、childrenが関数の場合は取得済みのdataのみを渡す
export default function QueryCheck<T>(props: Props<T>): React.JSX.Element {
  const { queries, data, title, children } = props

  const status = queries.find((q) => q.error !== null)?.error?.status ?? 200
  const render = (value: T): React.ReactNode => (typeof children === 'function' ? children(value) : children)

  return <ErrorCheck status={status}>{data === undefined ? <PageLoading title={title} /> : render(data)}</ErrorCheck>
}
