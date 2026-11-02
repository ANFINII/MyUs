import { useSuspenseQuery } from '@tanstack/react-query'
import { userQuery } from 'lib/query/options'
import PasswordChangeDone from './view'

export default function PasswordChangeDonePage(): React.JSX.Element {
  useSuspenseQuery(userQuery())

  return <PasswordChangeDone />
}
