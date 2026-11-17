import { useSuspenseQuery } from '@tanstack/react-query'
import { signupQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import Signup from './view'

export default function SignupPage(): React.JSX.Element {
  const router = useRouter()
  const token = String(router.query.token ?? '')
  const { data } = useSuspenseQuery(signupQuery(token))

  return <Signup token={token} email={data.email} />
}
