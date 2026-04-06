import { useRouter } from 'next/router'
import cx from 'utils/functions/cx'
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
      <h2 className={cx(style.error, 'mt_24')}>{content}</h2>
      <Button name="ログイン" className="mt_24 w_80" onClick={handleLogin} />
    </>
  )
}
