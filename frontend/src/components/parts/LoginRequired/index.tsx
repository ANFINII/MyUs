import clsx from 'clsx'

interface Props {
  isAuth: boolean
  margin?: string
  children: React.ReactNode
}

export default function LoginRequired(props: Props) {
  const { isAuth, margin, children } = props

  return <>{isAuth ? <>{children}</> : <h2 className={clsx('login_required', margin)}>ログインしてください</h2>}</>
}
