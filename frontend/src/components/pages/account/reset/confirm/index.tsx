import { useSuspenseQuery } from '@tanstack/react-query'
import { passwordResetVerifyQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ResetConfirm from './view'

export default function ResetConfirmPage(): React.JSX.Element {
  const router = useRouter()
  const token = String(router.query.token ?? '')
  const { data } = useSuspenseQuery(passwordResetVerifyQuery(token))

  return <ResetConfirm token={token} email={data.email} />
}
