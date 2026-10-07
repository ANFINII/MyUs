import { useTranslation } from 'react-i18next'
import { useRouter } from 'components/hooks/useRouter'
import Button from 'components/parts/Button'
import style from './Status.module.scss'

interface Props {
  content: string
}

export default function BackLogin(props: Props): React.JSX.Element {
  const { content } = props

  const router = useRouter()
  const { t } = useTranslation()

  const handleLogin = () => {
    router.push('/account/login')
  }

  return (
    <>
      <h2 className={style.error}>{content}</h2>
      <Button name={t('status.login')} className={style.button} onClick={handleLogin} />
    </>
  )
}
