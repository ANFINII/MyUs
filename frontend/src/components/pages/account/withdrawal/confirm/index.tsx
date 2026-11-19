import { useSuspenseQuery } from '@tanstack/react-query'
import { userQuery } from 'lib/query/options'
import WithdrawalConfirm from './view'

export default function WithdrawalConfirmPage(): React.JSX.Element {
  useSuspenseQuery(userQuery())

  return <WithdrawalConfirm />
}
