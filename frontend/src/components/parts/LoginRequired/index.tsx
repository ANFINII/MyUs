interface Props {
  children: React.ReactNode
}

export default function LoginRequired(props: Props) {
  const { children } = props

  const isAuth = true

  return <>{!isAuth ? <h2 className="login_required">ログインしてください</h2> : <>{children}</>}</>
}
