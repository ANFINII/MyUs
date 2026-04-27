import { useRouter } from 'next/router'
import Button from 'components/parts/Button'
import style from './Error.module.scss'

interface Props {
  content: string
}

export default function BackLogin(props: Props): React.JSX.Element {
  const { content } = props

  const router = useRouter()

  const handleLogin = () => {
    router.push('/account/login')
  }

  return (
    <>
      <h2 className={style.error}>{content}</h2>
      <Button name="ログイン" className={style.button} onClick={handleLogin} />
    </>
  )
}
