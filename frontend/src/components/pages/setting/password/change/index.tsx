import { useSuspenseQuery } from '@tanstack/react-query'
import { userQuery } from 'lib/query/options'
import PasswordChange from './view'

export default function PasswordChangePage(): React.JSX.Element {
  useSuspenseQuery(userQuery())

  return <PasswordChange />
}
