interface Props {
  isAuth: boolean
  children: React.ReactNode
}

export default function LoginRequired(props: Props) {
  const { isAuth, children } = props

  return <>{isAuth ? <>{children}</> : <h2 className="login_required">ログインしてください</h2>}</>
}
