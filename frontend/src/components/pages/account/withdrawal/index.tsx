import { useSuspenseQuery } from '@tanstack/react-query'
import { userQuery } from 'lib/query/options'
import Withdrawal from './view'

export default function WithdrawalPage(): React.JSX.Element {
  useSuspenseQuery(userQuery())

  return <Withdrawal />
}
