import { useTranslation } from 'react-i18next'
import { useAppRouter } from 'components/hooks/useAppRouter'
import Button from 'components/parts/Button'
import style from './Status.module.scss'

interface Props {
  content: string
}

export default function BackLogin(props: Props): React.JSX.Element {
  const { content } = props

  const { t } = useTranslation()
  const router = useAppRouter()

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
