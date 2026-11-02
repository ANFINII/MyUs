import { ErrorComponentProps } from '@tanstack/react-router'
import { isApiError } from 'lib/error'
import ErrorCheck from './Check'
import Custom500 from './Custom500'

export default function RouteError(props: ErrorComponentProps): React.JSX.Element {
  const { error } = props

  if (!isApiError(error)) return <Custom500 />
  return <ErrorCheck error={error}><></></ErrorCheck>
}
