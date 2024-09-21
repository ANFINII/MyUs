import clsx from 'clsx'
import { useUser } from 'components/hooks/useUser'

interface Props {
  margin?: string
  children: React.ReactNode
}

export default function LoginRequired(props: Props) {
  const { margin, children } = props

  const { user } = useUser()

  return <>{user.isActive ? <>{children}</> : <h2 className={clsx('login_required', margin)}>ログインしてください</h2>}</>
}
