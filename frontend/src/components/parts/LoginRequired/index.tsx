import clsx from 'clsx'
import { useUser } from 'components/hooks/useUser'
import style from './LoginRequired.module.scss'

interface Props {
  margin?: string
  children: React.ReactNode
}

export default function LoginRequired(props: Props) {
  const { margin, children } = props

  const { user } = useUser()

  return <>{user.isActive ? <>{children}</> : <h2 className={clsx(style.login_required, margin)}>ログインしてください</h2>}</>
}
