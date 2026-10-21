import { ApiError } from 'lib/error'
import Custom404 from './Custom404'
import Custom500 from './Custom500'
import Unauthorized from './Unauthorized'
import Unexpected from './Unexpected'

interface Props {
  error: ApiError | null
  children: React.ReactNode
}

export default function ErrorCheck(props: Props): React.JSX.Element {
  const { error, children } = props

  if (error === null) return <>{children}</>
  if (error.type === 'UNAUTHENTICATED') return <Unauthorized />
  if (error.type === 'NOT_FOUND') return <Custom404 />
  if (error.type === 'INTERNAL' || (error.type === undefined && error.status >= 500)) return <Custom500 />
  return <Unexpected />
}
