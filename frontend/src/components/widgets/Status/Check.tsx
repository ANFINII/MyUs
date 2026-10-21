import { ApiError } from 'lib/error'
import { ErrorType } from 'utils/constants/enum'
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
  if (error.type === ErrorType.Unauthenticated) return <Unauthorized />
  if (error.type === ErrorType.NotFound) return <Custom404 />
  if (error.type === ErrorType.Internal || error.status >= 500) return <Custom500 />
  return <Unexpected />
}
