import clsx from 'clsx'
import { useUser } from 'components/hooks/useUser'
import style from './Error.module.scss'

interface Props {
  margin?: string
  children: React.ReactNode
}

export default function LoginError(props: Props) {
  const { margin, children } = props

  const { user } = useUser()

  return (
    <>
      {user.isActive ? (
        <>{children}</>
      ) : (
        <h2 className={clsx(style.error, margin)}>ログインしてください</h2>
      )}
    </>
  )
}
